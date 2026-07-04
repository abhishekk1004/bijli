from django.db.models.signals import post_delete, post_save

from apps.common.cache import cache_invalidate
from apps.core.context_processors import NAV_CACHE_KEY
from apps.core.models import Client, CompanyInfo, HeroSlider, SocialMedia, Testimonial
from apps.core.views import HOME_CACHE_KEY
from apps.about.models import About, ChairmanMessage, Stat
from apps.services.models import Service
from apps.products.models import Category as ProductCategory
from apps.projects.models import Project

NAV_MODELS = (CompanyInfo, SocialMedia, Service, ProductCategory)
HOME_MODELS = (
    CompanyInfo, HeroSlider, About, ChairmanMessage, Service,
    Project, Client, Testimonial, Stat,
)


def _invalidate_nav_cache(sender, **kwargs):
    cache_invalidate(NAV_CACHE_KEY)


def _invalidate_home_cache(sender, **kwargs):
    cache_invalidate(HOME_CACHE_KEY)


def connect():
    for model in NAV_MODELS:
        post_save.connect(_invalidate_nav_cache, sender=model, weak=False)
        post_delete.connect(_invalidate_nav_cache, sender=model, weak=False)

    for model in HOME_MODELS:
        post_save.connect(_invalidate_home_cache, sender=model, weak=False)
        post_delete.connect(_invalidate_home_cache, sender=model, weak=False)
