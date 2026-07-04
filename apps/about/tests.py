from django.test import TestCase
from django.urls import reverse

from apps.about.models import About, ChairmanMessage, FAQ, TeamMember


class AboutModelTests(TestCase):
    def test_str_returns_title(self):
        about = About.objects.create(title='About CTS', slug='about-cts')
        self.assertEqual(str(about), 'About CTS')

    def test_chairman_message_is_singleton(self):
        ChairmanMessage.objects.create(name='Ram Sharma', message='Welcome to CTS.')
        with self.assertRaises(Exception):
            ChairmanMessage.objects.create(name='Someone Else', message='Duplicate.')


class AboutViewTests(TestCase):
    def setUp(self):
        About.objects.create(title='About CTS', slug='about-cts', is_active=True)
        TeamMember.objects.create(name='Hari Bahadur', designation='Engineer', is_active=True)
        FAQ.objects.create(question='What do you do?', answer='We build things.', is_active=True)

    def test_about_home_loads(self):
        response = self.client.get(reverse('about:home'))
        self.assertEqual(response.status_code, 200)

    def test_team_page_loads_and_lists_members(self):
        response = self.client.get(reverse('about:team'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hari Bahadur')

    def test_faq_page_loads_and_lists_questions(self):
        response = self.client.get(reverse('about:faq'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What do you do?')
