from django.db import models
from apps.core.models import SlugModel


class About(SlugModel):
    """Model for about page content"""
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Milestone(models.Model):
    """Model for company milestones"""
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
    """Model for statistics/numbers"""
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


class TeamMember(models.Model):
    """Model for team members"""
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


class FAQ(models.Model):
    """Model for FAQ items"""
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
