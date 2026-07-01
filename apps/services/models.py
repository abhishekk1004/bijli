from django.db import models
from apps.common.models import ActiveModel, SlugModel, OrderableModel
from apps.common.utils import upload_to


class ServiceCategory(ActiveModel, SlugModel, OrderableModel):
    """Service category model."""
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Service(ActiveModel, SlugModel, OrderableModel):
    """Service model."""
    
    name = models.CharField(max_length=200)
    
    ICON_CHOICES = [
        ('flaticon-warehouse', 'Warehouse'),
        ('flaticon-power', 'Power'),
        ('flaticon-security', 'Security'),
        ('flaticon-maintenance', 'Maintenance'),
        ('flaticon-networking', 'Networking'),
        ('flaticon-surveillance', 'Surveillance'),
        ('flaticon-installation', 'Installation'),
        ('flaticon-support', 'Support'),
    ]
    
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='flaticon-warehouse')
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    features = models.TextField(blank=True, help_text='Comma-separated list of features')
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_features_list(self):
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []
