from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from apps.core.sitemaps import SITEMAPS
from apps.core.views import robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),

    path('', include('apps.core.urls', namespace='core')),
    path('about/', include('apps.about.urls', namespace='about')),
    path('services/', include('apps.services.urls', namespace='services')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('projects/', include('apps.projects.urls', namespace='projects')),
    path('gallery/', include('apps.gallery.urls', namespace='gallery')),
    path('contact/', include('apps.contact.urls', namespace='contact')),
    path('api/', include('apps.api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'apps.core.views.handler403'
handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
