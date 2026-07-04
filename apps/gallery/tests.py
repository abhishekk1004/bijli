from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.gallery.models import Album, GalleryImage

ONE_PX_GIF = SimpleUploadedFile(
    'pixel.gif', b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
    content_type='image/gif',
)


class AlbumModelTests(TestCase):
    def test_str_returns_title(self):
        album = Album.objects.create(title='Site Visits', slug='site-visits')
        self.assertEqual(str(album), 'Site Visits')


class GalleryViewTests(TestCase):
    def setUp(self):
        self.album = Album.objects.create(title='Site Visits', slug='site-visits', is_active=True)
        GalleryImage.objects.create(album=self.album, image=ONE_PX_GIF, caption='Team on site')

    def test_gallery_home_loads_and_lists_album(self):
        response = self.client.get(reverse('gallery:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site Visits')

    def test_album_detail_loads(self):
        response = self.client.get(reverse('gallery:album', args=[self.album.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team on site')

    def test_album_detail_404_for_unknown_slug(self):
        response = self.client.get(reverse('gallery:album', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)

    def test_inactive_album_is_hidden_from_list(self):
        self.album.is_active = False
        self.album.save()
        response = self.client.get(reverse('gallery:home'))
        self.assertNotContains(response, 'Site Visits')
