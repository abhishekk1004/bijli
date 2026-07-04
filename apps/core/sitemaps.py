from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.services.models import Service
from apps.products.models import Product
from apps.projects.models import Project
from apps.gallery.models import Album


class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('services:detail', args=[obj.slug])


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('products:detail', args=[obj.slug])


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('projects:detail', args=[obj.slug])


class AlbumSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Album.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('gallery:album', args=[obj.slug])


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        return ['core:home', 'about:home', 'services:home', 'products:home', 'projects:home', 'contact:home']

    def location(self, item):
        return reverse(item)


SITEMAPS = {
    'static': StaticViewSitemap,
    'services': ServiceSitemap,
    'products': ProductSitemap,
    'projects': ProjectSitemap,
    'gallery': AlbumSitemap,
}
