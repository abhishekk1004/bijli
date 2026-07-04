import os
import uuid

from django.utils.text import slugify


def upload_to(instance, filename):
    """Generates unique upload path."""
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    model_name = instance.__class__.__name__.lower()
    return os.path.join(model_name, filename)


def generate_unique_slug(instance, slug_field='slug', max_length=255):
    """Generate a unique slug for the given model instance."""
    title = getattr(instance, 'title', None) or str(instance)
    slug = slugify(title)
    model_class = instance.__class__
    # Use _base_manager to get unfiltered queryset (not affected by custom managers)
    queryset = model_class._base_manager.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    unique_slug = slug
    counter = 1

    while queryset.filter(**{slug_field: unique_slug}).exists():
        suffix = f'-{counter}'
        unique_slug = f'{slug[:max_length - len(suffix)]}{suffix}'
        counter += 1

    return unique_slug
