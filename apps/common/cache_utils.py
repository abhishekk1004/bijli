from django.core.cache import cache
from django.conf import settings


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 60)  # 1 hour default


def cache_get_or_set(key, callback, ttl=CACHE_TTL):
    """
    Get value from cache or execute callback and cache result.
    
    Args:
        key: Cache key
        callback: Function to execute if cache miss
        ttl: Cache time-to-live in seconds
    
    Returns:
        Cached or computed value
    """
    value = cache.get(key)
    if value is None:
        value = callback()
        cache.set(key, value, ttl)
    return value


def cache_invalidate(*keys):
    """
    Invalidate multiple cache keys.
    
    Args:
        *keys: Variable number of cache keys to invalidate
    """
    for key in keys:
        cache.delete(key)


def cache_invalidate_pattern(pattern):
    """
    Invalidate all cache keys matching a pattern.
    
    Note: This requires Redis as cache backend.
    
    Args:
        pattern: Pattern to match (e.g., 'company_*')
    """
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('default')
        keys = redis_conn.keys(pattern)
        if keys:
            redis_conn.delete(*keys)
    except Exception:
        pass