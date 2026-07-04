from django.db import models

from apps.common.models import ActiveModel, SlugModel, OrderableModel, TimeStampedModel, WebPImageMixin
from apps.common.utils import upload_to


class Album(ActiveModel, SlugModel, OrderableModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta(OrderableModel.Meta):
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.title


class GalleryImage(TimeStampedModel, OrderableModel, WebPImageMixin):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)
    caption = models.CharField(max_length=255, blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.caption or f"{self.album.title} - Image {self.order}"


class GalleryVideo(TimeStampedModel, OrderableModel):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    title = models.CharField(max_length=200)
    video_url = models.URLField(help_text='YouTube/Vimeo embed URL')
    thumbnail = models.ImageField(upload_to=upload_to, blank=True, null=True)

    class Meta(OrderableModel.Meta):
        verbose_name = 'Gallery Video'
        verbose_name_plural = 'Gallery Videos'

    def __str__(self):
        return self.title
