from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Job


class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def find(self, tag, **attrs):
        return next(values for name, values in self.tags
                    if name == tag and all(values.get(k) == v for k, v in attrs.items()))


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class SEOTests(TestCase):
    def setUp(self):
        Job.objects.all().delete()
        self.jobs = [Job.objects.create(
            title=title, company=company, date_range='2026',
            description=('Build secure systems with clients and deliver reliable software. ' * 5),
        ) for title, company in [('Engineer', 'Example & Co'), ('Developer', 'Other company')]]

    def tags(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        return Tags(response.content.decode())

    def test_home_title_and_social_metadata_on_every_page(self):
        response = self.client.get('/')
        self.assertContains(response, '<title>Cameron J. Davis — Forward Deployed Engineer</title>', html=True)
        for path in ['/', *(reverse('detail', args=[job.pk]) for job in self.jobs)]:
            with self.subTest(path=path):
                tags = self.tags(path)
                absolute = 'https://cjdswe.dev' + path
                self.assertEqual(tags.find('link', rel='canonical')['href'], absolute)
                self.assertEqual(tags.find('meta', property='og:url')['content'], absolute)
                self.assertEqual(tags.find('meta', property='og:image')['content'],
                                 'https://cjdswe.dev/static/cameron-hero.jpg')
                self.assertEqual(tags.find('meta', property='og:type')['content'], 'website')
                self.assertEqual(tags.find('meta', name='twitter:card')['content'], 'summary_large_image')
                self.assertEqual(tags.find('meta', property='og:description')['content'],
                                 tags.find('meta', name='description')['content'])
                self.assertTrue(tags.find('meta', property='og:title')['content'])

    def test_detail_descriptions_are_distinct_and_truncated_at_word_boundary(self):
        descriptions = []
        for job in self.jobs:
            tags = self.tags(reverse('detail', args=[job.pk]))
            description = tags.find('meta', name='description')['content']
            prefix = f'{job.title} at {job.company}. '
            self.assertTrue(description.startswith(prefix))
            excerpt = description[len(prefix):]
            self.assertLessEqual(len(excerpt), 150)
            self.assertTrue(excerpt.endswith('…'))
            self.assertIn(excerpt[:-1] + ' ', job.description)
            descriptions.append(description)
        self.assertNotEqual(*descriptions)

    def test_robots(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'Sitemap: https://cjdswe.dev/sitemap.xml')
        self.assertContains(response, 'Allow: /')
        self.assertContains(response, 'Disallow: /admin/')

    def test_sitemap_lists_home_and_each_job(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        root = ElementTree.fromstring(response.content)
        urls = [element.text for element in root.findall('{*}url/{*}loc')]
        self.assertCountEqual(urls, ['https://cjdswe.dev/', *(
            'https://cjdswe.dev' + reverse('detail', args=[job.pk]) for job in self.jobs)])

    def test_root_icons_redirect_to_static(self):
        for filename in ['favicon.ico', 'apple-touch-icon.png']:
            self.assertRedirects(self.client.get('/' + filename), '/static/' + filename,
                                 status_code=302, fetch_redirect_response=False)

    def test_hero_markup_and_removed_png_references(self):
        tags = self.tags('/')
        image = tags.find('img', **{'class': 'hero-image'})
        self.assertEqual((image['width'], image['height']), ('1672', '941'))
        self.assertEqual(image['fetchpriority'], 'high')
        self.assertTrue(image['src'].endswith('cameron-hero.jpg'))
        source = tags.find('source', type='image/webp')
        self.assertIn('cameron-hero-900.webp 900w', source['srcset'])
        self.assertIn('cameron-hero.webp 1672w', source['srcset'])
        self.assertEqual(source['sizes'], '100vw')
        old_name = 'cameron-hero' + '.png'
        self.assertFalse((settings.BASE_DIR / 'jobs/static' / old_name).exists())
        for path in (settings.BASE_DIR / 'jobs/templates').rglob('*'):
            if path.is_file():
                self.assertNotIn(old_name, path.read_text())

    def test_media_cache_control_with_temporary_media_root(self):
        with TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            Path(directory, 'example.txt').write_text('media example')
            response = self.client.get('/media/example.txt')
            try:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['Cache-Control'], 'public, max-age=86400')
                self.assertEqual(b''.join(response.streaming_content), b'media example')
            finally:
                response.close()
