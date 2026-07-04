from django.test import TestCase
from django.urls import reverse

from apps.services.models import Service, ServiceCategory


class ServiceModelTests(TestCase):
    def test_features_list_splits_on_comma(self):
        service = Service.objects.create(
            name='BTS Rollout', slug='bts-rollout',
            short_description='Tower rollouts', description='Full description',
            features='Site survey, Installation, Commissioning',
        )
        self.assertEqual(service.get_features_list(), ['Site survey', 'Installation', 'Commissioning'])

    def test_str_returns_name(self):
        service = Service.objects.create(
            name='Consultancy', slug='consultancy',
            short_description='x', description='y',
        )
        self.assertEqual(str(service), 'Consultancy')


class ServiceViewTests(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name='Telecom', slug='telecom')
        self.service = Service.objects.create(
            name='BTS Rollout', slug='bts-rollout', category=self.category,
            short_description='Tower rollouts', description='Full description',
            is_active=True,
        )

    def test_services_list_loads(self):
        response = self.client.get(reverse('services:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BTS Rollout')

    def test_service_detail_loads(self):
        response = self.client.get(reverse('services:detail', args=[self.service.slug]))
        self.assertEqual(response.status_code, 200)

    def test_service_detail_404_for_unknown_slug(self):
        response = self.client.get(reverse('services:detail', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)

    def test_inactive_service_returns_404(self):
        self.service.is_active = False
        self.service.save()
        response = self.client.get(reverse('services:detail', args=[self.service.slug]))
        self.assertEqual(response.status_code, 404)

    def test_category_filter_loads(self):
        response = self.client.get(reverse('services:category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
