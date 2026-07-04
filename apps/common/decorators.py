from functools import wraps

from django.core.cache import cache
from django.http import HttpResponseForbidden


def ratelimit_post(key_prefix: str, limit: int = 5, window: int = 300):
    """Fixed-window rate limit per client IP, applied to POST requests only.

    Blocks with 403 once `limit` POSTs from the same IP land within `window` seconds.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR', 'unknown')
                cache_key = f'ratelimit:{key_prefix}:{ip}'
                count = cache.get(cache_key)
                if count is None:
                    cache.set(cache_key, 1, window)
                elif count >= limit:
                    return HttpResponseForbidden('Too many submissions. Please try again later.')
                else:
                    cache.incr(cache_key)
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
