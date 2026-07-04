from django.conf import settings
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60)

# Sentinel so a cached None isn't mistaken for a cache miss.
_CACHE_MISS = object()


def cache_get_or_set(key, callback, ttl=CACHE_TTL):
    value = cache.get(key, _CACHE_MISS)
    if value is _CACHE_MISS:
        value = callback()
        cache.set(key, value, ttl)
    return value


def cache_invalidate(*keys):
    for key in keys:
        cache.delete(key)
