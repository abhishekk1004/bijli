from django.db import models
from apps.common.models import ActiveModel, SlugModel, OrderableModel, SEOModel, TimeStampedModel, WebPImageMixin
from apps.common.utils import upload_to


class ProjectStatus(models.TextChoices):
    ONGOING = 'ongoing', 'Ongoing'
    EXECUTED = 'executed', 'Executed'


class Category(ActiveModel, SlugModel, OrderableModel):

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(ActiveModel, SlugModel, OrderableModel, SEOModel, WebPImageMixin):

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    client = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ONGOING, db_index=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
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

    def get_scope_list(self):
        if self.scope_of_work:
            return [s.strip() for s in self.scope_of_work.split(',')]
        return []


class ProjectImage(TimeStampedModel, OrderableModel, WebPImageMixin):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=upload_to)
    caption = models.CharField(max_length=255, blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    def __str__(self):
        return f"{self.project.name} - Image {self.order}"
