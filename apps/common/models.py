import uuid

from django.db import models


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