from django.test import TestCase
from django.urls import reverse

from apps.projects.models import Category, Project, ProjectStatus


class ProjectModelTests(TestCase):
    def test_scope_list_splits_on_comma(self):
        project = Project.objects.create(
            name='NT GSM Rollout', slug='nt-gsm-rollout', client='Ncell',
            short_description='GSM network rollout', description='Full description',
            location='Kathmandu', scope_of_work='Survey, Installation, Testing',
        )
        self.assertEqual(project.get_scope_list(), ['Survey', 'Installation', 'Testing'])

    def test_default_status_is_ongoing(self):
        project = Project.objects.create(
            name='NT GSM Rollout', slug='nt-gsm-rollout-2', client='Ncell',
            short_description='x', description='y', location='Kathmandu',
        )
        self.assertEqual(project.status, ProjectStatus.ONGOING)


class ProjectViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Telecom', slug='telecom')
        self.ongoing = Project.objects.create(
            name='NT GSM Rollout', slug='nt-gsm-rollout', client='Ncell', category=self.category,
            short_description='x', description='y', location='Kathmandu',
            status=ProjectStatus.ONGOING, is_active=True,
        )
        self.executed = Project.objects.create(
            name='Huawei BTS Install', slug='huawei-bts-install', client='Huawei', category=self.category,
            short_description='x', description='y', location='Pokhara',
            status=ProjectStatus.EXECUTED, is_active=True,
        )

    def test_projects_list_loads(self):
        response = self.client.get(reverse('projects:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NT GSM Rollout')
        self.assertContains(response, 'Huawei BTS Install')

    def test_status_filter_returns_only_matching_projects(self):
        response = self.client.get(reverse('projects:home'), {'status': 'ongoing'})
        self.assertContains(response, 'NT GSM Rollout')
        self.assertNotContains(response, 'Huawei BTS Install')

    def test_project_detail_loads(self):
        response = self.client.get(reverse('projects:detail', args=[self.ongoing.slug]))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_404_for_unknown_slug(self):
        response = self.client.get(reverse('projects:detail', args=['does-not-exist']))
        self.assertEqual(response.status_code, 404)
