"""
About App URLs
"""
from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.AboutView.as_view(), name='home'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('faq/', views.FAQView.as_view(), name='faq'),
]