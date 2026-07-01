from django.shortcuts import render
from django.views.generic import TemplateView

from apps.services.models import Service
from apps.products.models import Product
from apps.about.models import TeamMember
from apps.core.models import HeroSlider, Client, Testimonial


class HomeView(TemplateView):
    """Home page view with all sections."""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Hero Slides
        context['hero_slides'] = HeroSlider.objects.filter(is_active=True)[:5]
        
        # Services (limited to 6 for homepage)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        
        # Products (limited to 4 for homepage)
        context['products'] = Product.objects.filter(is_active=True)[:4]
        
        # Clients
        context['clients'] = Client.objects.filter(is_active=True)[:8]
        
        # Testimonials
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:5]
        
        return context


def handler404(request, exception):
    """Custom 404 error handler."""
    return render(request, 'core/error.html', {
        'error_code': '404',
        'error_title': 'Page Not Found',
        'error_message': 'Sorry, the page you are looking for does not exist or has been moved.'
    }, status=404)


def handler500(request):
    """Custom 500 error handler."""
    return render(request, 'core/error.html', {
        'error_code': '500',
        'error_title': 'Server Error',
        'error_message': 'Sorry, something went wrong. Please try again later.'
    }, status=500)


def handler403(request, exception):
    """Custom 403 error handler."""
    return render(request, 'core/error.html', {
        'error_code': '403',
        'error_title': 'Access Forbidden',
        'error_message': 'Sorry, you do not have permission to access this page.'
    }, status=403)
