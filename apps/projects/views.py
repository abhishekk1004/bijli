from django.shortcuts import render, get_object_or_404
from apps.projects.models import Project, Category, ProjectStatus
from apps.core.models import Testimonial


def projects_home(request):
    projects = Project.objects.filter(is_active=True).select_related('category').order_by('-created_at')
    status = request.GET.get('status')
    if status in ProjectStatus.values:
        projects = projects.filter(status=status)
    categories = Category.objects.filter(is_active=True)

    context = {
        'projects': projects[:12],
        'categories': categories,
        'current_category': None,
        'current_status': status,
        'project_statuses': ProjectStatus.choices,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'projects/projects.html', context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('gallery_images'),
        slug=slug, is_active=True,
    )

    related_projects = Project.objects.filter(
        category=project.category,
        is_active=True
    ).select_related('category').exclude(pk=project.pk)[:4]

    context = {
        'project': project,
        'related_projects': related_projects,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
        'meta_title': project.get_meta_title(),
        'meta_description': project.get_meta_description() or project.short_description,
        'meta_image': project.image,
    }
    return render(request, 'projects/project_detail.html', context)


def category_projects(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    projects = Project.objects.filter(category=category, is_active=True).select_related('category').order_by('-created_at')
    categories = Category.objects.filter(is_active=True)

    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category,
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, 'projects/projects.html', context)
