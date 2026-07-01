from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from apps.services.models import Service
from apps.core.models import Testimonial


class ServiceListView(ListView):
    """Services list view."""
    model = Service
    template_name = 'services/services.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True)
        return context


class ServiceDetailView(DetailView):
    """Service detail view."""
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            is_active=True,
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:5]
        return context


# Function-based views for URL patterns
def services_home(request):
    """Services home page."""
    services = Service.objects.filter(is_active=True)
    categories = ServiceCategory.objects.filter(is_active=True)
    
    return render(request, 'services/services.html', {
        'services': services,
        'categories': categories,
    })


def service_detail(request, slug):
    """Service detail page."""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        is_active=True,
        category=service.category
    ).exclude(id=service.id)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:5]
    
    return render(request, 'services/service_detail.html', {
        'service': service,
        'related_services': related_services,
        'testimonials': testimonials,
    })


def category_services(request, slug):
    """Services by category."""
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    services = Service.objects.filter(category=category, is_active=True)
    categories = ServiceCategory.objects.filter(is_active=True)
    
    return render(request, 'services/services.html', {
        'services': services,
        'categories': categories,
        'current_category': category,
    })
