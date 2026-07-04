from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_home, name='home'),
    path('<slug:slug>/', views.album_detail, name='album'),
]
