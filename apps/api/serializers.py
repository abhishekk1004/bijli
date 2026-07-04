from rest_framework import serializers

from apps.about.models import ChairmanMessage, Stat
from apps.contact.models import Contact
from apps.core.models import CompanyInfo, Testimonial
from apps.gallery.models import Album, GalleryImage, GalleryVideo
from apps.products.models import Category as ProductCategory
from apps.products.models import Product, ProductImage
from apps.projects.models import Category as ProjectCategory
from apps.projects.models import Project, ProjectImage
from apps.services.models import Service, ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['name', 'slug', 'description', 'icon']


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_slug = serializers.SlugRelatedField(
        source='category', slug_field='slug', queryset=ServiceCategory.objects.all(),
        write_only=True, required=False, allow_null=True,
    )
    features = serializers.ListField(source='get_features_list', child=serializers.CharField(), read_only=True)

    class Meta:
        model = Service
        fields = [
            'name', 'slug', 'category', 'category_slug', 'short_description', 'description',
            'icon', 'image', 'features', 'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        extra_kwargs = {'is_active': {'default': True}}


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'description', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'caption', 'order']


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_slug = serializers.SlugRelatedField(
        source='category', slug_field='slug', queryset=ProductCategory.objects.all(),
        write_only=True, required=False, allow_null=True,
    )
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    features = serializers.ListField(source='features_list', child=serializers.CharField(), read_only=True)
    specifications = serializers.ListField(source='specifications_list', child=serializers.CharField(), read_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'category_slug', 'short_description', 'description',
            'image', 'gallery_images', 'price', 'features', 'specifications',
            'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['name', 'slug', 'description']


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'order']


class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer(read_only=True)
    category_slug = serializers.SlugRelatedField(
        source='category', slug_field='slug', queryset=ProjectCategory.objects.all(),
        write_only=True, required=False, allow_null=True,
    )
    gallery_images = ProjectImageSerializer(many=True, read_only=True)
    scope_of_work = serializers.ListField(source='get_scope_list', child=serializers.CharField(), read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'name', 'slug', 'category', 'category_slug', 'client', 'status', 'status_display',
            'short_description', 'description', 'image', 'gallery_images', 'location',
            'start_date', 'end_date', 'scope_of_work', 'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['image', 'caption', 'order']


class GalleryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryVideo
        fields = ['title', 'video_url', 'thumbnail', 'order']


class AlbumSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)
    videos = GalleryVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['title', 'slug', 'description', 'cover_image', 'images', 'videos', 'is_active', 'order']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['client_name', 'company', 'designation', 'image', 'message', 'rating', 'is_active']


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = [
            'company_name', 'short_name', 'tagline', 'logo', 'favicon',
            'email', 'phone', 'secondary_phone', 'address', 'google_map', 'copyright',
        ]


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ['number', 'label', 'icon', 'order']


class ChairmanMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChairmanMessage
        fields = ['name', 'designation', 'photo', 'message']


class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message', 'service_interest', 'product_interest']
