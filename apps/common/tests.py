from django.core.cache import cache
from django.test import TestCase, override_settings

from apps.common.cache import cache_get_or_set
from apps.about.models import About
from apps.common.utils import generate_unique_slug

LOCMEM_CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}


@override_settings(CACHES=LOCMEM_CACHES)
class CacheGetOrSetTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_callback_runs_once_for_repeated_calls(self):
        calls = []

        def callback():
            calls.append(1)
            return 'value'

        self.assertEqual(cache_get_or_set('test:key', callback), 'value')
        self.assertEqual(cache_get_or_set('test:key', callback), 'value')
        self.assertEqual(len(calls), 1)

    def test_falsy_but_not_none_values_are_still_cached(self):
        calls = []

        def callback():
            calls.append(1)
            return []

        cache_get_or_set('test:falsy', callback)
        cache_get_or_set('test:falsy', callback)
        self.assertEqual(len(calls), 1)


class GenerateUniqueSlugTests(TestCase):
    def test_appends_suffix_on_collision(self):
        About.objects.create(title='About Us', slug='about-us')
        second = About(title='About Us')
        slug = generate_unique_slug(second, 'slug')
        self.assertNotEqual(slug, 'about-us')
        self.assertTrue(slug.startswith('about-us'))
