import importlib
import os
from unittest import mock

from django.contrib import admin
from django.test import SimpleTestCase, TestCase, override_settings

from .models import Job, Project


class SettingsLogicTests(SimpleTestCase):
    def test_security_settings_in_production_and_development(self):
        from portfolio import settings as project_settings

        # Reload the module itself: override_settings doesn't rerun its logic.
        # Never load a developer's .env while exercising environment settings.
        with mock.patch.dict(os.environ, {'PYTHON_DOTENV_DISABLED': '1'}):
            try:
                for debug in (False, True):
                    with self.subTest(DEBUG=debug), mock.patch.dict(
                        os.environ, {'DJANGO_DEBUG': str(debug)}
                    ):
                        config = importlib.reload(project_settings)
                        self.assertEqual(config.DEBUG, debug)
                        self.assertEqual(config.SESSION_COOKIE_SECURE, not debug)
                        self.assertEqual(config.CSRF_COOKIE_SECURE, not debug)
                        self.assertEqual(config.SECURE_HSTS_SECONDS, 0 if debug else 86400)
                        self.assertFalse(config.SECURE_HSTS_INCLUDE_SUBDOMAINS)
                        self.assertFalse(config.SECURE_HSTS_PRELOAD)
                        self.assertEqual(
                            config.CSRF_TRUSTED_ORIGINS,
                            [] if debug else ['https://cjdswe.dev', 'https://www.cjdswe.dev'],
                        )
                        self.assertEqual(config.ALLOWED_HOSTS, [
                            '127.0.0.1', 'localhost', 'cjdswe-portfolio.onrender.com',
                            'cjdswe.dev', 'www.cjdswe.dev',
                        ])
                        self.assertNotIn('SECURE_SSL_REDIRECT', vars(config))
                        self.assertNotIn('SECURE_PROXY_SSL_HEADER', vars(config))
            finally:
                importlib.reload(project_settings)

    def test_admin_registration_and_order_editing(self):
        for model, columns in (
            (Job, ('title', 'company', 'date_range', 'order')),
            (Project, ('name', 'url', 'order')),
        ):
            with self.subTest(model=model):
                self.assertTrue(admin.site.is_registered(model))
                model_admin = admin.site.get_model_admin(model)
                self.assertEqual(model_admin.list_display, columns)
                self.assertEqual(model_admin.list_editable, ('order',))


@override_settings(
    DEBUG=False,
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class SecurityResponseTests(TestCase):
    def test_homepage_csp_in_both_debug_modes(self):
        for debug in (False, True):
            with self.subTest(DEBUG=debug), override_settings(DEBUG=debug):
                response = self.client.get('/', HTTP_HOST='localhost')
                self.assertEqual(response.status_code, 200)
                policy = dict(
                    directive.split(' ', 1)
                    for directive in response.headers['Content-Security-Policy'].split('; ')
                )
                self.assertEqual(policy, {
                    'default-src': "'self'",
                    'script-src': "'self'",
                    'style-src': "'self' https://fonts.googleapis.com 'unsafe-inline'",
                    'font-src': 'https://fonts.gstatic.com',
                    'img-src': "'self' https://cdn.jsdelivr.net data:",
                    'connect-src': "'self'",
                    'frame-ancestors': "'none'",
                    'base-uri': "'self'",
                    'form-action': "'self'",
                    'object-src': "'none'",
                })
                self.assertNotIn('Content-Security-Policy-Report-Only', response.headers)

    def test_host_allowlist(self):
        self.assertEqual(self.client.get('/', HTTP_HOST='evil.example').status_code, 400)
        self.assertEqual(
            self.client.get('/', HTTP_HOST='cjdswe-portfolio.onrender.com').status_code,
            200,
        )

    def test_admin_login_has_csp(self):
        response = self.client.get('/admin/login/', HTTP_HOST='localhost')
        self.assertEqual(response.status_code, 200)
        self.assertIn("default-src 'self'", response.headers['Content-Security-Policy'])
