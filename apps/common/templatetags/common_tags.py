from django import template

register = template.Library()


def _resolve_url(obj, field_name, spec_field_name):
    source = getattr(obj, field_name, None)
    if not source:
        return ''
    spec_field = getattr(obj, spec_field_name, None)
    try:
        return spec_field.url if spec_field else source.url
    except (ValueError, OSError):
        return source.url


@register.simple_tag
def webp_image(obj, field_name='image'):
    """URL of the full-size WebP rendition of `obj.<field_name>`, falling back to the original."""
    return _resolve_url(obj, field_name, f'{field_name}_webp')


@register.simple_tag
def webp_thumb(obj, field_name='image'):
    """URL of the WebP thumbnail rendition of `obj.<field_name>`, falling back to the original."""
    return _resolve_url(obj, field_name, f'{field_name}_thumbnail')
