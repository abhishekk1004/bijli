from django.db import models
from apps.core.models import SlugModel
from apps.common.models import ActiveModel, SingletonModel, WebPImageMixin
from apps.common.utils import upload_to


class About(ActiveModel, SlugModel):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Milestone(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year} - {self.title}"


class Stat(models.Model):
    number = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Stat'
        verbose_name_plural = 'Stats'
        ordering = ['order', 'label']

    def __str__(self):
        return f"{self.number} - {self.label}"


class TeamMember(WebPImageMixin, models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class ChairmanMessage(SingletonModel, ActiveModel):
    """Chairman's message shown on the About page. Restricted to a single row."""
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, default='Chairman')
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)
    message = models.TextField()

    class Meta:
        verbose_name = "Chairman's Message"
        verbose_name_plural = "Chairman's Message"

    def __str__(self):
        return f"{self.name} - {self.designation}"


class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question
