from rest_framework import generics, viewsets
from rest_framework.throttling import AnonRateThrottle

from apps.api.permissions import IsAdminOrReadOnly
from apps.api.serializers import (
    AlbumSerializer, ChairmanMessageSerializer, CompanyInfoSerializer,
    ContactCreateSerializer, ProductSerializer, ProjectSerializer,
    ServiceSerializer, StatSerializer, TestimonialSerializer,
)
from apps.about.models import ChairmanMessage, Stat
from apps.contact.services import notify_new_contact
from apps.core.models import CompanyInfo, Testimonial
from apps.gallery.models import Album
from apps.products.models import Product
from apps.projects.models import Project
from apps.services.models import Service


class SubmissionThrottle(AnonRateThrottle):
    scope = 'submissions'


class ActiveFilterMixin:
    """Anonymous callers only see active rows; staff see everything."""

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_authenticated and user.is_staff):
            queryset = queryset.filter(is_active=True)
        return queryset


class ServiceViewSet(ActiveFilterMixin, viewsets.ModelViewSet):
    queryset = Service.objects.select_related('category')
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = {'category__slug': ['exact'], 'is_featured': ['exact']}
    search_fields = ['name', 'short_description', 'description']
    ordering_fields = ['order', 'name', 'created_at']


class ProductViewSet(ActiveFilterMixin, viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('gallery_images')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = {'category__slug': ['exact'], 'is_featured': ['exact']}
    search_fields = ['name', 'short_description', 'description']
    ordering_fields = ['order', 'name', 'price', 'created_at']


class ProjectViewSet(ActiveFilterMixin, viewsets.ModelViewSet):
    queryset = Project.objects.select_related('category').prefetch_related('gallery_images')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = {'category__slug': ['exact'], 'status': ['exact'], 'is_featured': ['exact']}
    search_fields = ['name', 'client', 'location', 'short_description', 'description']
    ordering_fields = ['order', 'name', 'created_at']


class AlbumViewSet(ActiveFilterMixin, viewsets.ModelViewSet):
    queryset = Album.objects.prefetch_related('images', 'videos')
    serializer_class = AlbumSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title', 'created_at']


class TestimonialViewSet(ActiveFilterMixin, viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['client_name', 'company', 'message']
    ordering_fields = ['rating', 'created_at']


class CompanyInfoView(generics.RetrieveAPIView):
    serializer_class = CompanyInfoSerializer

    def get_object(self):
        return generics.get_object_or_404(CompanyInfo, is_active=True)


class ChairmanMessageView(generics.RetrieveAPIView):
    serializer_class = ChairmanMessageSerializer

    def get_object(self):
        return generics.get_object_or_404(ChairmanMessage, is_active=True)


class StatListView(generics.ListAPIView):
    queryset = Stat.objects.filter(is_active=True)
    serializer_class = StatSerializer
    pagination_class = None
    filter_backends = []


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactCreateSerializer
    throttle_classes = [SubmissionThrottle]

    def perform_create(self, serializer):
        contact = serializer.save()
        notify_new_contact(contact)
