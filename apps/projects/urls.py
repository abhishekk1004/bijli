"""
Projects App URLs
"""
from django.urls import path
from apps.projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects_home, name='home'),
    path('category/<slug:slug>/', views.category_projects, name='category'),
    path('<slug:slug>/', views.project_detail, name='detail'),
]