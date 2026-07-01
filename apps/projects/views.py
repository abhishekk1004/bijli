from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from apps.projects.models import Project, Category
from apps.core.models import Testimonial


class ProjectListView(ListView):
    """View for listing all projects"""
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_active=True).order_by('-created_at')
        
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


class ProjectDetailView(DetailView):
    """View for displaying project details"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    query_pk_and_slug = True
    
    def get_queryset(self):
        return Project.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get related projects (same category, excluding current)
        context['related_projects'] = Project.objects.filter(
            category=project.category,
            is_active=True
        ).exclude(pk=project.pk)[:4]
        
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        return context


def projects_home(request):
    """Function-based view for projects home"""
    projects = Project.objects.filter(is_active=True).order_by('-created_at')[:12]
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': None,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'projects/projects.html', context)


def project_detail(request, slug):
    """Function-based view for project detail"""
    project = get_object_or_404(Project, slug=slug, is_active=True)
    
    related_projects = Project.objects.filter(
        category=project.category,
        is_active=True
    ).exclude(pk=project.pk)[:4]
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'projects/project_detail.html', context)


def category_projects(request, slug):
    """Function-based view for projects by category"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    projects = Project.objects.filter(category=category, is_active=True).order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'projects/projects.html', context)
