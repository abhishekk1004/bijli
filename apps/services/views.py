from django.shortcuts import render, get_object_or_404

from apps.services.models import Service, ServiceCategory
from apps.core.models import Testimonial


def services_home(request):
    services = Service.objects.filter(is_active=True).select_related('category')
    categories = ServiceCategory.objects.filter(is_active=True)

    return render(request, 'services/services.html', {
        'services': services,
        'categories': categories,
    })


def service_detail(request, slug):
    service = get_object_or_404(Service.objects.select_related('category'), slug=slug, is_active=True)
    related_services = Service.objects.filter(
        is_active=True,
        category=service.category
    ).select_related('category').exclude(id=service.id)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:5]

    return render(request, 'services/service_detail.html', {
        'service': service,
        'related_services': related_services,
        'testimonials': testimonials,
        'meta_title': service.get_meta_title(),
        'meta_description': service.get_meta_description() or service.short_description,
        'meta_image': service.image,
    })


def category_services(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    services = Service.objects.filter(category=category, is_active=True).select_related('category')
    categories = ServiceCategory.objects.filter(is_active=True)

    return render(request, 'services/services.html', {
        'services': services,
        'categories': categories,
        'current_category': category,
    })
