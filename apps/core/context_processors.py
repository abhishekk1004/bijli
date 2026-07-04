from apps.core.models import CompanyInfo, SocialMedia
from apps.services.models import Service
from apps.products.models import Category
from apps.common.cache import cache_get_or_set

NAV_CACHE_KEY = 'core:nav_context'
NAV_CACHE_TTL = 60 * 15


def _build_nav_context() -> dict:
    return {
        'company': CompanyInfo.objects.filter(is_active=True).first(),
        'services': list(Service.objects.filter(is_active=True)[:10]),
        'product_categories': list(Category.objects.filter(is_active=True)[:10]),
        'social_links': list(SocialMedia.objects.filter(is_active=True)),
        'footer_services': list(Service.objects.filter(is_active=True)[:6]),
    }


def company_context(request):
    """Navbar/footer variables, cached as a whole since this runs on every request."""
    return cache_get_or_set(NAV_CACHE_KEY, _build_nav_context, ttl=NAV_CACHE_TTL)
