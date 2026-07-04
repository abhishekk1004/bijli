from django.db import models
from apps.common.models import ActiveModel, SlugModel, OrderableModel, SEOModel, TimeStampedModel, WebPImageMixin
from apps.common.utils import upload_to


class Category(ActiveModel, SlugModel, OrderableModel):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Product(ActiveModel, SlugModel, OrderableModel, SEOModel, WebPImageMixin):
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.TextField(blank=True, help_text='Comma-separated list of features')
    specifications = models.TextField(blank=True, help_text='Comma-separated list of specifications')
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',') if f.strip()]
        return []
    
    @property
    def specifications_list(self):
        if self.specifications:
            return [s.strip() for s in self.specifications.split(',') if s.strip()]
        return []
    
    def get_features_list(self):
        return self.features_list

    def get_specifications_list(self):
        return self.specifications_list


class ProductImage(TimeStampedModel, OrderableModel, WebPImageMixin):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=upload_to)
    caption = models.CharField(max_length=255, blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"
