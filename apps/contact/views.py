from django.shortcuts import render, redirect
from django.contrib import messages
from apps.contact.models import Contact
from apps.services.models import Service
from apps.products.models import Product


def contact_home(request):
    """Contact page view with form handling"""
    services = Service.objects.filter(is_active=True)[:6]
    products = Product.objects.filter(is_active=True)[:6]
    
    context = {
        'services': services,
        'products': products,
    }
    return render(request, 'contact/contact.html', context)


def contact_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        service_interest = request.POST.get('service_interest')
        product_interest = request.POST.get('product_interest')
        
        # Create contact entry
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            service_interest=service_interest if service_interest else None,
            product_interest=product_interest if product_interest else None,
        )
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact:home')
    
    return redirect('contact:home')
