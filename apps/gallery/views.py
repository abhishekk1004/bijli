from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from apps.gallery.models import Album


def gallery_home(request):
    albums = Album.objects.filter(is_active=True).annotate(
        image_count=Count('images', distinct=True),
        video_count=Count('videos', distinct=True),
    )
    return render(request, 'gallery/gallery.html', {'albums': albums})


def album_detail(request, slug):
    album = get_object_or_404(
        Album.objects.prefetch_related('images', 'videos'),
        slug=slug, is_active=True,
    )
    return render(request, 'gallery/album_detail.html', {'album': album})
