from django.shortcuts import render, get_object_or_404
from apps.products.models import Product, Category
from apps.core.models import Testimonial


def products_home(request):
    products = Product.objects.filter(is_active=True).select_related('category').order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
        'current_category': None,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'products/products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('gallery_images'),
        slug=slug, is_active=True,
    )

    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).select_related('category').exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
        'meta_title': product.get_meta_title(),
        'meta_description': product.get_meta_description() or product.short_description,
        'meta_image': product.image,
        'og_type': 'product',
    }
    return render(request, 'products/product_detail.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True).select_related('category').order_by('-created_at')
    categories = Category.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'products/products.html', context)
