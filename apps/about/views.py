from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.about.models import About, Milestone, Stat, TeamMember, FAQ
from apps.services.models import Service
from apps.products.models import Product
from apps.projects.models import Project


class AboutView(TemplateView):
    """About page view."""
    template_name = 'about/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # About content
        context['about'] = About.objects.filter(is_active=True).first()
        context['milestones'] = Milestone.objects.filter(is_active=True)
        context['stats'] = Stat.objects.filter(is_active=True)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        
        # Counts
        context['services_count'] = Service.objects.filter(is_active=True).count()
        context['products_count'] = Product.objects.filter(is_active=True).count()
        context['projects_count'] = Project.objects.filter(is_active=True).count()
        context['team_count'] = TeamMember.objects.filter(is_active=True).count()
        
        return context


class TeamView(ListView):
    """Team members listing view."""
    model = TeamMember
    template_name = 'about/team.html'
    context_object_name = 'team_members'
    
    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)


class FAQView(TemplateView):
    """FAQ page view."""
    template_name = 'about/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context
