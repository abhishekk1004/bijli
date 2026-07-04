from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.contact.models import Contact
from apps.services.models import Service, ServiceCategory

LOCMEM_CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

User = get_user_model()


def make_service(name: str, slug: str, category=None, is_active: bool = True, **extra) -> Service:
    return Service.objects.create(
        name=name, slug=slug, category=category,
        short_description=f'{name} summary', description=f'{name} description',
        is_active=is_active, **extra,
    )


@override_settings(CACHES=LOCMEM_CACHES, CELERY_TASK_ALWAYS_EAGER=True)
class PublicReadApiTests(APITestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name='Telecom', slug='telecom')
        self.active = make_service('BTS Rollout', 'bts-rollout', category=self.category, is_featured=True)
        self.inactive = make_service('Hidden Service', 'hidden-service', is_active=False)
        make_service('Consultancy', 'consultancy')

    def test_anonymous_list_is_paginated_and_hides_inactive(self):
        response = self.client.get('/api/v1/services/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        slugs = [row['slug'] for row in response.data['results']]
        self.assertIn('bts-rollout', slugs)
        self.assertNotIn('hidden-service', slugs)

    def test_detail_lookup_is_by_slug(self):
        response = self.client.get('/api/v1/services/bts-rollout/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'BTS Rollout')
        self.assertNotIn('id', response.data)

    def test_inactive_detail_is_404_for_anonymous(self):
        response = self.client.get('/api/v1/services/hidden-service/')
        self.assertEqual(response.status_code, 404)

    def test_category_filter(self):
        response = self.client.get('/api/v1/services/', {'category__slug': 'telecom'})
        slugs = [row['slug'] for row in response.data['results']]
        self.assertEqual(slugs, ['bts-rollout'])

    def test_search(self):
        response = self.client.get('/api/v1/services/', {'search': 'Consultancy'})
        slugs = [row['slug'] for row in response.data['results']]
        self.assertEqual(slugs, ['consultancy'])


@override_settings(CACHES=LOCMEM_CACHES, CELERY_TASK_ALWAYS_EAGER=True)
class JwtWriteApiTests(APITestCase):
    def setUp(self):
        self.staff = User.objects.create_user('editor', 'editor@example.com', 'pass12345', is_staff=True)
        self.regular = User.objects.create_user('visitor', 'visitor@example.com', 'pass12345')

    def _token_for(self, username: str) -> str:
        response = self.client.post(reverse('api:token'), {'username': username, 'password': 'pass12345'})
        self.assertEqual(response.status_code, 200)
        return response.data['access']

    def test_anonymous_write_is_rejected(self):
        response = self.client.post('/api/v1/services/', {'name': 'X', 'slug': 'x'})
        self.assertEqual(response.status_code, 401)

    def test_non_staff_write_is_forbidden(self):
        token = self._token_for('visitor')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/v1/services/', {'name': 'X', 'slug': 'x'})
        self.assertEqual(response.status_code, 403)

    def test_staff_can_create_service_with_jwt(self):
        token = self._token_for('editor')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/v1/services/', {
            'name': 'New Service', 'slug': 'new-service',
            'short_description': 'Summary', 'description': 'Description',
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Service.objects.filter(slug='new-service').exists())

    def test_staff_sees_inactive_rows(self):
        make_service('Hidden Service', 'hidden-service', is_active=False)
        token = self._token_for('editor')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/v1/services/hidden-service/')
        self.assertEqual(response.status_code, 200)

    def test_token_refresh_flow(self):
        response = self.client.post(reverse('api:token'), {'username': 'editor', 'password': 'pass12345'})
        refresh = response.data['refresh']
        response = self.client.post(reverse('api:token_refresh'), {'refresh': refresh})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)


@override_settings(CACHES=LOCMEM_CACHES, CELERY_TASK_ALWAYS_EAGER=True)
class SubmissionApiTests(APITestCase):
    def test_contact_submission_creates_row(self):
        response = self.client.post('/api/v1/contact/', {
            'name': 'Bishnu Thapa', 'email': 'bishnu@example.com', 'phone': '+977-9800000000',
            'subject': 'Inquiry', 'message': 'Please send a quote.',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.count(), 1)

    def test_contact_submission_requires_fields(self):
        response = self.client.post('/api/v1/contact/', {'name': 'X'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Contact.objects.count(), 0)
