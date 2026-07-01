"""
Products App URLs
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_home, name='home'),
    path('category/<slug:slug>/', views.category_products, name='category'),
    path('<slug:slug>/', views.product_detail, name='detail'),
]