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
    slug = slugify(getattr(instance, 'title') or str(instance))
    model_class = instance.__class__
    queryset = model_class.objects.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    unique_slug = slug
    counter = 1

    while queryset.filter(**{slug_field: unique_slug}).exists():
        suffix = f'-{counter}'
        unique_slug = f'{slug[:max_length - len(suffix)]}{suffix}'
        counter += 1

    return unique_slug


def generate_uuid() -> str:
    """Generate a short UUID string."""
    return str(uuid.uuid4())[:8]


def compress_image(image, quality=85, max_width=1920, max_height=1080):
    """Compress and resize an image."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(image)
    
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output


def convert_to_webp(image, quality=85):
    """Convert image to WebP format."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(image)
    
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    output = BytesIO()
    img.save(output, format='WEBP', quality=quality, optimize=True)
    output.seek(0)
    
    return output


def generate_thumbnail(image, size=(300, 300), quality=80):
    """Generate a thumbnail from an image."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(image)
    
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output