from html.parser import HTMLParser
from pathlib import Path

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Job, Project


class NavigationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.navs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'button':
            self.buttons.append(dict(attrs))
        elif tag == 'nav':
            self.navs.append(dict(attrs))


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class PortfolioTests(TestCase):
    def setUp(self):
        # Data migrations seed portfolio content; each test controls its own rows.
        Job.objects.all().delete()
        Project.objects.all().delete()

    def test_home_with_empty_database(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Experience will be added soon.')
        self.assertContains(response, 'Projects will be added soon.')

    def test_home_lists_jobs_and_projects_in_order(self):
        later_job = Job.objects.create(
            title='Later role', company='Later company', date_range='2025',
            description='Later job description', order=20,
        )
        earlier_job = Job.objects.create(
            title='Earlier role', company='Earlier company', date_range='2024',
            description='Earlier job description', order=10,
        )
        later_project = Project.objects.create(
            name='Later project', description='Later project description', order=20,
        )
        earlier_project = Project.objects.create(
            name='Earlier project', description='Earlier project description', order=10,
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['jobs'], [earlier_job, later_job])
        self.assertQuerySetEqual(response.context['projects'], [earlier_project, later_project])
        html = response.content.decode()
        for earlier, later in [
            (earlier_job.title, later_job.title),
            (earlier_project.name, later_project.name),
        ]:
            self.assertContains(response, earlier)
            self.assertContains(response, later)
            self.assertLess(html.index(earlier), html.index(later))

    def test_home_document_structure_and_removed_demo(self):
        response = self.client.get(reverse('home'))
        html = response.content.decode().lower()
        for closing_tag in ['</main>', '</body>', '</html>']:
            self.assertEqual(html.count(closing_tag), 1)
        self.assertLess(html.index('</main>'), html.index('<footer'))
        self.assertLess(html.index('</footer>'), html.index('</body>'))
        self.assertNotIn('throughline', html)
        self.assertNotIn('bootstrap.bundle', html)
        self.assertNotIn('<script src="http', html)

    def test_home_menu_controls_primary_navigation(self):
        response = self.client.get(reverse('home'))
        parser = NavigationParser()
        parser.feed(response.content.decode())
        buttons = [button for button in parser.buttons if 'menu-toggle' in button.get('class', '').split()]
        self.assertEqual(len(buttons), 1)
        button = buttons[0]
        self.assertEqual(button.get('type'), 'button')
        self.assertEqual(button.get('aria-expanded'), 'false')
        navs = [nav for nav in parser.navs if nav.get('aria-label') == 'Primary navigation']
        self.assertEqual(len(navs), 1)
        self.assertTrue(navs[0].get('id'))
        self.assertEqual(button.get('aria-controls'), navs[0]['id'])
        self.assertContains(response, '>Menu</button>')

    def test_existing_job_detail(self):
        job = Job.objects.create(
            title='Engineer', company='Example company', date_range='2024',
            description='Build useful systems',
        )
        response = self.client.get(reverse('detail', args=[job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, job.title)
        self.assertContains(response, job.company)

    def test_missing_job_detail(self):
        self.assertEqual(self.client.get(reverse('detail', args=[999])).status_code, 404)

    def test_throughline_is_unavailable(self):
        self.assertEqual(self.client.get('/throughline/').status_code, 404)

    def test_media_does_not_expose_project_files(self):
        self.assertNotEqual(settings.MEDIA_ROOT, settings.BASE_DIR)
        self.assertNotEqual(Path(settings.MEDIA_ROOT).resolve(), Path(settings.BASE_DIR).resolve())
        for path in ['/media/manage.py', '/media/db.sqlite3', '/media/portfolio/settings.py']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)
