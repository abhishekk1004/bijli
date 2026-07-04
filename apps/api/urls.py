from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.api import views

app_name = 'api'

router = DefaultRouter()
router.register('services', views.ServiceViewSet, basename='service')
router.register('products', views.ProductViewSet, basename='product')
router.register('projects', views.ProjectViewSet, basename='project')
router.register('albums', views.AlbumViewSet, basename='album')
router.register('testimonials', views.TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='docs'),

    path('v1/company/', views.CompanyInfoView.as_view(), name='company'),
    path('v1/chairman-message/', views.ChairmanMessageView.as_view(), name='chairman_message'),
    path('v1/stats/', views.StatListView.as_view(), name='stats'),
    path('v1/contact/', views.ContactCreateView.as_view(), name='contact'),
    path('v1/', include(router.urls)),
]
