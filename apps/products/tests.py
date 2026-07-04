from django.test import TestCase
from django.urls import reverse

from apps.products.models import Category, Product


class ProductModelTests(TestCase):
    def test_features_and_specifications_lists(self):
        product = Product.objects.create(
            name='Solar Panel 300W', slug='solar-panel-300w',
            short_description='High-efficiency panel', description='Full description',
            features='Weatherproof, 25-year warranty',
            specifications='300W, Monocrystalline',
        )
        self.assertEqual(product.features_list, ['Weatherproof', '25-year warranty'])
        self.assertEqual(product.specifications_list, ['300W', 'Monocrystalline'])


class ProductViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electrical Equipment', slug='electrical-equipment')
        self.product = Product.objects.create(
            name='Solar Panel 300W', slug='solar-panel-300w', category=self.category,
            short_description='High-efficiency panel', description='Full description',
            is_active=True,
        )

    def test_products_list_loads(self):
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Solar Panel 300W')

    def test_product_detail_loads(self):
        response = self.client.get(reverse('products:detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_404_for_unknown_slug(self):
        response = self.client.get(reverse('products:detail', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)

    def test_category_filter_loads(self):
        response = self.client.get(reverse('products:category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
