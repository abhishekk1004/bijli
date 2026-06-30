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
    # Safely read title using getattr with fallback to str(instance)
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


def generate_uuid() -> str:
    """Generate a short UUID string."""
    return str(uuid.uuid4())[:8]


def compress_image(image, quality=85, max_width=1920, max_height=1080):
    """Compress and resize an image."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(image)
    
    # Convert any non-RGB mode to RGB (handles RGBA, L, P, etc.)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    # For RGBA, keep transparency; for others convert to RGB
    if img.mode == 'RGBA':
        # Create RGB background and paste RGBA on it
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])
        img = rgb_img
    
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output


def convert_to_webp(image, quality=85):
    """Convert image to WebP format, preserving transparency."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(image)
    
    # WebP supports transparency, so only convert non-RGB non-RGBA modes
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGBA')
    
    output = BytesIO()
    # WebP format preserves alpha channel when using 'RGBA' mode
    img.save(output, format='WEBP', quality=quality, optimize=True)
    output.seek(0)
    
    return output


def generate_thumbnail(image, size=(300, 300), quality=80):
    """Generate a thumbnail from an image."""
    from PIL import Image
    from io import BytesIO

    img = Image.open(image)
    
    # Convert any non-RGB mode to RGB (handles RGBA, L, P, etc.)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    # For RGBA, keep transparency; for others convert to RGB
    if img.mode == 'RGBA':
        # Create RGB background and paste RGBA on it
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3])
        img = rgb_img
    
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output