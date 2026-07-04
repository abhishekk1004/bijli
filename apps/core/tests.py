from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.core.models import CompanyInfo


def make_company(**overrides):
    defaults = {
        'company_name': 'Celltronic Tele Solutions',
        'email': 'info@cts.example',
        'phone': '+977-1-5000000',
        'address': 'Satdobato, Lalitpur, Nepal',
        'copyright': 'CTS Group',
    }
    defaults.update(overrides)
    return CompanyInfo.objects.create(**defaults)


class CompanyInfoTests(TestCase):
    def test_str_returns_company_name(self):
        company = make_company()
        self.assertEqual(str(company), 'Celltronic Tele Solutions')

    def test_second_instance_is_rejected(self):
        make_company()
        with self.assertRaises(ValidationError):
            make_company(company_name='Another Company')

    def test_load_returns_the_singleton(self):
        company = make_company()
        self.assertEqual(CompanyInfo.load(), company)


class HomeViewTests(TestCase):
    def setUp(self):
        self.company = make_company()

    def test_home_page_loads(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_includes_company_from_context_processor(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.context['company'], self.company)

    def test_home_page_renders_with_no_data_at_all(self):
        CompanyInfo.objects.all().delete()
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)


class RobotsAndSitemapTests(TestCase):
    def test_robots_txt_lists_sitemap(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sitemap:', response.content)

    def test_sitemap_xml_loads(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
