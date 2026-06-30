from django.db import models


class ActiveManager(models.Manager):
    """Manager that returns only active objects."""

    def active(self):
        return self.get_queryset().filter(is_active=True)


class AllObjectsManager(models.Manager):
    """Manager that returns all objects including inactive."""

    pass


class BaseManager(models.Manager):
    """Custom manager with common query methods."""

    def get_active(self):
        return self.get_queryset().filter(is_active=True)

    def get_by_slug(self, slug):
        return self.get_queryset().filter(slug=slug).first()