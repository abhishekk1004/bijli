from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from apps.products.models import Product, Category
from apps.core.models import Testimonial


class ProductListView(ListView):
    """View for listing all products"""
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).order_by('-created_at')
        
        # Filter by category if provided
        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['current_category'] = None
        
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        return context


class ProductDetailView(DetailView):
    """View for displaying product details"""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    query_pk_and_slug = True
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get related products (same category, excluding current)
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(pk=product.pk)[:4]
        
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        return context


def products_home(request):
    """Function-based view for products home"""
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': None,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'products/products.html', context)


def product_detail(request, slug):
    """Function-based view for product detail"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'products/product_detail.html', context)


def category_products(request, slug):
    """Function-based view for products by category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True).order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'products/products.html', context)
