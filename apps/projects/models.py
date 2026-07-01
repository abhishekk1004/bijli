from django.db import models
from apps.common.models import ActiveModel, SlugModel, OrderableModel
from apps.common.utils import upload_to


class Category(ActiveModel, SlugModel, OrderableModel):
    """Project category model."""
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Project(ActiveModel, SlugModel, OrderableModel):
    """Project model."""
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    client = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    gallery = models.TextField(blank=True, help_text='Comma-separated list of image URLs')
    location = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    scope_of_work = models.TextField(blank=True, help_text='Comma-separated list of scope items')
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_gallery_list(self):
        if self.gallery:
            return [img.strip() for img in self.gallery.split(',')]
        return []
    
    def get_scope_list(self):
        if self.scope_of_work:
            return [s.strip() for s in self.scope_of_work.split(',')]
        return []
