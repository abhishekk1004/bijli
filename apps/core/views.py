from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.services.models import Service
from apps.products.models import Product
from apps.about.models import About, ChairmanMessage, TeamMember, Stat
from apps.projects.models import Project
from apps.core.models import HeroSlider, Client, Testimonial
from apps.common.cache import cache_get_or_set

HOME_CACHE_KEY = 'core:home_context'
HOME_CACHE_TTL = 60 * 15


def build_home_context() -> dict:
    """Assemble the homepage context. Cached as a whole to avoid the ~9 queries on every hit."""
    return {
        'hero_slides': list(HeroSlider.objects.filter(is_active=True)[:5]),
        'about': About.objects.filter(is_active=True).first(),
        'chairman_message': ChairmanMessage.load(),
        'services': list(Service.objects.filter(is_active=True).select_related('category')[:6]),
        'products': list(Product.objects.filter(is_active=True).select_related('category')[:4]),
        'featured_projects': list(
            Project.objects.filter(is_active=True, is_featured=True).select_related('category')[:3]
        ),
        'clients': list(Client.objects.filter(is_active=True)[:8]),
        'testimonials': list(Testimonial.objects.filter(is_active=True)[:5]),
        'stats': list(Stat.objects.filter(is_active=True)[:6]),
    }


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(cache_get_or_set(HOME_CACHE_KEY, build_home_context, ttl=HOME_CACHE_TTL))
        return context


def handler404(request, exception):
    return render(request, 'core/error.html', {
        'error_code': '404',
        'error_title': 'Page Not Found',
        'error_message': 'Sorry, the page you are looking for does not exist or has been moved.'
    }, status=404)


def handler500(request):
    return render(request, 'core/error.html', {
        'error_code': '500',
        'error_title': 'Server Error',
        'error_message': 'Sorry, something went wrong. Please try again later.'
    }, status=500)


def handler403(request, exception):
    return render(request, 'core/error.html', {
        'error_code': '403',
        'error_title': 'Access Forbidden',
        'error_message': 'Sorry, you do not have permission to access this page.'
    }, status=403)


def robots_txt(request: HttpRequest) -> HttpResponse:
    """Serve robots.txt pointing crawlers to the sitemap."""
    lines = [
        'User-Agent: *',
        'Disallow: /admin/',
        'Disallow: /media/private/',
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')
