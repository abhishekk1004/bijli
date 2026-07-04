import uuid

from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class WebPSpec(ImageSpec):
    """Compressed WebP rendition capped at 1920px, used in place of the original upload."""
    processors = [ResizeToFit(1920, 1920, upscale=False)]
    format = 'WEBP'
    options = {'quality': 82}


class ThumbnailSpec(ImageSpec):
    """Small WebP thumbnail for cards/grids/lazy-loaded lists."""
    processors = [ResizeToFit(400, 400, upscale=False)]
    format = 'WEBP'
    options = {'quality': 75}


class TimeStampedModel(models.Model):
    """Abstract base model with UUID primary key and timestamps."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        abstract = True
        ordering = ['-created_at']


class ActiveModel(TimeStampedModel):
    """Abstract base model with active/inactive status."""

    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Is Active')

    class Meta(TimeStampedModel.Meta):
        abstract = True


class SlugModel(models.Model):
    """Abstract base model with auto-generated slug."""

    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Abstract base model for SEO fields."""

    meta_title = models.CharField(
        max_length=70, blank=True, null=True, verbose_name='Meta Title'
    )
    meta_description = models.TextField(
        max_length=160, blank=True, null=True, verbose_name='Meta Description'
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Meta Keywords'
    )

    class Meta:
        abstract = True

    def get_meta_title(self) -> str:
        return self.meta_title or str(self)

    def get_meta_description(self) -> str:
        return self.meta_description or ''


class OrderableModel(models.Model):
    """Abstract base model with ordering field."""

    order = models.PositiveIntegerField(default=0, verbose_name='Order')

    class Meta:
        abstract = True
        ordering = ['order']


class WebPImageMixin(models.Model):
    """Adds compressed WebP + thumbnail renditions derived from an `image` field."""

    image_webp = ImageSpecField(source='image', spec=WebPSpec)
    image_thumbnail = ImageSpecField(source='image', spec=ThumbnailSpec)

    class Meta:
        abstract = True


class WebPLogoMixin(models.Model):
    """Adds compressed WebP + thumbnail renditions derived from a `logo` field."""

    logo_webp = ImageSpecField(source='logo', spec=WebPSpec)
    logo_thumbnail = ImageSpecField(source='logo', spec=ThumbnailSpec)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """Abstract mixin that restricts a model to a single database row."""

    # DB-enforced guard: makes the "only one row" invariant hold even when the
    # exists()-then-save() check below races under concurrent requests.
    singleton_guard = models.PositiveSmallIntegerField(default=1, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # self.pk is unreliable here: UUID primary keys are assigned a default at
        # instantiation time, not at save time, so it's already set on a fresh instance.
        if self._state.adding and type(self).objects.exists():
            raise ValidationError(f'Only one {type(self).__name__} instance is allowed.')
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # The exists()-then-save() check above can race under concurrent
            # requests; catch the DB-level unique constraint violation on
            # singleton_guard and normalise it to the same ValidationError
            # shape callers expect.
            raise ValidationError(f'Only one {type(self).__name__} instance is allowed.')

    @classmethod
    def load(cls):
        return cls.objects.first()