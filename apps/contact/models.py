from django.db import models

from apps.common.models import ActiveModel, OrderableModel, TimeStampedModel


class Contact(TimeStampedModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    service_interest = models.CharField(max_length=200, blank=True, null=True)
    product_interest = models.CharField(max_length=200, blank=True, null=True)
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class BranchOffice(ActiveModel, OrderableModel):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    google_map = models.URLField(blank=True, help_text='Google Maps embed URL')
    is_head_office = models.BooleanField(default=False)

    class Meta(OrderableModel.Meta):
        verbose_name = 'Branch Office'
        verbose_name_plural = 'Branch Offices'

    def __str__(self):
        return self.name
