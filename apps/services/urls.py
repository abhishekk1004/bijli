from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_home, name='home'),
    path('category/<slug:slug>/', views.category_services, name='category'),
    path('<slug:slug>/', views.service_detail, name='detail'),
]