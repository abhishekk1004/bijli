from django.shortcuts import render, redirect
from django.contrib import messages
from apps.contact.models import Contact
from apps.services.models import Service
from apps.products.models import Product
import re


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
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        service_interest = request.POST.get('service_interest', '').strip()
        product_interest = request.POST.get('product_interest', '').strip()
        
        errors = []
        
        if not name:
            errors.append('Name is required.')
        elif len(name) < 2:
            errors.append('Name must be at least 2 characters.')
        
        if not email:
            errors.append('Email is required.')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address.')
        
        if not phone:
            errors.append('Phone number is required.')
        elif not re.match(r'^[\d\s\-\+\(\)]{7,20}$', phone):
            errors.append('Please enter a valid phone number.')
        
        if not subject:
            errors.append('Subject is required.')
        elif len(subject) < 3:
            errors.append('Subject must be at least 3 characters.')
        
        if not message:
            errors.append('Message is required.')
        elif len(message) < 10:
            errors.append('Message must be at least 10 characters.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('contact:home')
        
        Contact.objects.create(
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
