from django.db import models


class ActiveManager(models.Manager):
    """Manager that returns only active objects."""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def active(self):
        """Convenience alias that returns the already-filtered queryset."""
        return self.get_queryset()
