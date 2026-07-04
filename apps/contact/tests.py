from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.contact.models import BranchOffice, Contact

LOCMEM_CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

VALID_CONTACT_PAYLOAD = {
    'name': 'Bishnu Thapa',
    'email': 'bishnu@example.com',
    'phone': '+977-9800000000',
    'subject': 'Project Inquiry',
    'message': 'We would like a quote for a BTS installation.',
}


@override_settings(CACHES=LOCMEM_CACHES)
class ContactFormTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_valid_submission_creates_contact_and_redirects(self):
        response = self.client.post(reverse('contact:submit'), VALID_CONTACT_PAYLOAD)
        self.assertRedirects(response, reverse('contact:home'))
        self.assertEqual(Contact.objects.count(), 1)

    def test_missing_required_field_does_not_create_contact(self):
        payload = {**VALID_CONTACT_PAYLOAD, 'message': ''}
        response = self.client.post(reverse('contact:submit'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)

    def test_invalid_email_is_rejected(self):
        payload = {**VALID_CONTACT_PAYLOAD, 'email': 'not-an-email'}
        self.client.post(reverse('contact:submit'), payload)
        self.assertEqual(Contact.objects.count(), 0)

    def test_repeated_submissions_are_rate_limited(self):
        for _ in range(5):
            self.client.post(reverse('contact:submit'), VALID_CONTACT_PAYLOAD)
        response = self.client.post(reverse('contact:submit'), VALID_CONTACT_PAYLOAD)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Contact.objects.count(), 5)


@override_settings(CACHES=LOCMEM_CACHES)
class BranchOfficeTests(TestCase):
    def test_active_branches_render_on_contact_page(self):
        BranchOffice.objects.create(name='Head Office', address='Satdobato, Lalitpur', is_head_office=True)
        response = self.client.get(reverse('contact:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Head Office')


@override_settings(
    CACHES=LOCMEM_CACHES,
    CELERY_TASK_ALWAYS_EAGER=True,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    ADMIN_NOTIFICATION_EMAIL='admin@cts.example',
)
class NotificationTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_contact_submission_sends_admin_email(self):
        from django.core import mail

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(reverse('contact:submit'), VALID_CONTACT_PAYLOAD)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['admin@cts.example'])
        self.assertIn('Project Inquiry', mail.outbox[0].subject)

    def test_broker_failure_does_not_break_submission(self):
        from unittest.mock import patch

        with patch('apps.contact.services.send_contact_notification.delay', side_effect=RuntimeError('broker down')):
            with self.captureOnCommitCallbacks(execute=True):
                response = self.client.post(reverse('contact:submit'), VALID_CONTACT_PAYLOAD)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)
