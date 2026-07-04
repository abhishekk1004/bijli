import re

from django.contrib import messages
from django.shortcuts import redirect, render

from apps.common.decorators import ratelimit_post
from apps.contact.models import BranchOffice, Contact
from apps.contact.services import notify_new_contact
from apps.products.models import Product
from apps.services.models import Service

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_RE = re.compile(r'^[\d\s\-\+\(\)]{7,20}$')


def contact_home(request):
    context = {
        'services': Service.objects.filter(is_active=True)[:6],
        'products': Product.objects.filter(is_active=True)[:6],
        'branch_offices': BranchOffice.objects.filter(is_active=True),
    }
    return render(request, 'contact/contact.html', context)


@ratelimit_post('contact_submit', limit=5, window=300)
def contact_submit(request):
    if request.method != 'POST':
        return redirect('contact:home')

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
    elif len(name) > 200:
        errors.append('Name must be at most 200 characters.')

    if not email:
        errors.append('Email is required.')
    elif not EMAIL_RE.match(email):
        errors.append('Please enter a valid email address.')

    if not phone:
        errors.append('Phone number is required.')
    elif not PHONE_RE.match(phone):
        errors.append('Please enter a valid phone number.')

    if not subject:
        errors.append('Subject is required.')
    elif len(subject) < 3:
        errors.append('Subject must be at least 3 characters.')
    elif len(subject) > 200:
        errors.append('Subject must be at most 200 characters.')

    if not message:
        errors.append('Message is required.')
    elif len(message) < 10:
        errors.append('Message must be at least 10 characters.')

    if errors:
        for error in errors:
            messages.error(request, error)
        return render(request, 'contact/contact.html', {
            'services': Service.objects.filter(is_active=True)[:6],
            'products': Product.objects.filter(is_active=True)[:6],
            'branch_offices': BranchOffice.objects.filter(is_active=True),
            'form_data': {
                'name': name, 'email': email, 'phone': phone, 'subject': subject,
                'message': message, 'service_interest': service_interest,
                'product_interest': product_interest,
            },
        })

    contact = Contact.objects.create(
        name=name, email=email, phone=phone, subject=subject, message=message,
        service_interest=service_interest or None,
        product_interest=product_interest or None,
    )
    notify_new_contact(contact)

    messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
    return redirect('contact:home')
