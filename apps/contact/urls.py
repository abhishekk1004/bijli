from django.urls import path
from apps.contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_home, name='home'),
    path('submit/', views.contact_submit, name='submit'),
]