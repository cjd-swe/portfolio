import importlib
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase, override_settings


SEED = '0004_seed_experience_and_projects'
BEFORE_SEED = '0003_project_skill_alter_job_options_remove_job_image_and_more'
LATEST = '0005_correct_ibm_start_date'


class DataMigrationTests(TransactionTestCase):
    def setUp(self):
        media = tempfile.TemporaryDirectory()
        self.addCleanup(media.cleanup)
        settings = override_settings(MEDIA_ROOT=media.name)
        settings.enable()
        self.addCleanup(settings.disable)
        # Restore the schema even when a test fails, before removing its media.
        self.addCleanup(self.migrate, LATEST)
        # Rows left by earlier tests (e.g. edited seed rows a reverse correctly keeps)
        # would block unapplying 0003, which re-adds a NOT NULL column.
        from jobs.models import Job, Project
        Job.objects.all().delete()
        Project.objects.all().delete()
        self.migrate(None)
        self.apps = self.migrate(BEFORE_SEED)
        self.seed = importlib.import_module(f'jobs.migrations.{SEED}')
        self.dates = importlib.import_module(f'jobs.migrations.{LATEST}')

    def migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([('jobs', target)])
        if target is not None:
            return executor.loader.project_state([('jobs', target)]).apps

    def test_zero_to_latest_preserves_seed_content_and_logos(self):
        self.migrate(None)
        apps = self.migrate(LATEST)
        Job = apps.get_model('jobs', 'Job')
        Project = apps.get_model('jobs', 'Project')
        self.assertEqual(Job.objects.count(), 3)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(list(Job.objects.values_list('company', 'date_range')), [
            ('Artium AI', 'Mar 2026 – Present'),
            ('IBM', 'Aug 2021 – Dec 2025'),
            ('CAMUVA Mobile', '2017 – 2022'),
        ])
        for seed in self.seed.JOBS:
            expected = seed.copy()
            filename = expected.pop('logo_filename')
            if expected['company'] == 'IBM':
                expected['date_range'] = 'Aug 2021 – Dec 2025'
            job = Job.objects.get(**expected)
            if filename:
                self.assertEqual(job.logo.name, f'static/job_logos/{filename}')
                with job.logo.open('rb') as saved:
                    self.assertEqual(
                        saved.read(), (Path(self.seed.LOGO_DIR) / filename).read_bytes(),
                    )
            else:
                self.assertFalse(job.logo)
        for expected in self.seed.PROJECTS:
            self.assertTrue(Project.objects.filter(**expected).exists())

    def test_forward_can_run_twice_without_resaving_logos(self):
        Job = self.apps.get_model('jobs', 'Job')
        Project = self.apps.get_model('jobs', 'Project')
        with connection.schema_editor() as editor:
            self.seed.seed_data(self.apps, editor)
            original = list(Job.objects.values())
            storage = Job._meta.get_field('logo').storage
            with patch.object(storage, 'save', side_effect=AssertionError('Logo resaved')):
                self.seed.seed_data(self.apps, editor)
        self.assertEqual(list(Job.objects.values()), original)
        self.assertEqual(Job.objects.count(), 3)
        self.assertEqual(Project.objects.count(), 2)
        self.assertTrue(all('logo_filename' in seed for seed in self.seed.JOBS))

    def test_reverse_preserves_edited_and_unrelated_rows_and_their_logos(self):
        Job = self.apps.get_model('jobs', 'Job')
        Project = self.apps.get_model('jobs', 'Project')
        unrelated = Job.objects.create(
            company='IBM', title='Unrelated role', date_range='2020',
            description='Pre-existing row',
        )
        unrelated_project = Project.objects.create(
            name='SharpWatch (CAPFREE)', description='Pre-existing project',
        )
        # Its matching name prevents get_or_create from creating this project.
        apps = self.migrate(SEED)
        Job = apps.get_model('jobs', 'Job')
        Project = apps.get_model('jobs', 'Project')
        edited = Job.objects.get(company='Artium AI')
        kept_logo = Path(edited.logo.path)
        edited.description = 'Edited description'
        edited.save()
        removed_logo = Path(Job.objects.get(company='IBM', title='Software Engineer').logo.path)
        edited_project = Project.objects.get(name='Spotify Mood Ring')
        edited_project.url = 'https://example.com/edited'
        edited_project.save()
        self.migrate(BEFORE_SEED)
        self.assertSetEqual(set(Job.objects.values_list('pk', flat=True)), {unrelated.pk, edited.pk})
        self.assertSetEqual(
            set(Project.objects.values_list('pk', flat=True)),
            {unrelated_project.pk, edited_project.pk},
        )
        self.assertTrue(kept_logo.exists())
        self.assertFalse(removed_logo.exists())

    def test_date_correction_and_reverse_only_match_seeded_title_and_date(self):
        apps = self.migrate(SEED)
        Job = apps.get_model('jobs', 'Job')
        seeded = Job.objects.get(company='IBM')
        other_rows = [
            Job.objects.create(company=company, title=title, date_range=date, description='Other')
            for company, title, date in [
                ('IBM', 'Manager', self.dates.OLD_DATE_RANGE),
                ('IBM', 'Manager', self.dates.NEW_DATE_RANGE),
                ('IBM', 'Software Engineer', '2010 – 2011'),
                ('Other company', 'Software Engineer', self.dates.OLD_DATE_RANGE),
                ('Other company', 'Software Engineer', self.dates.NEW_DATE_RANGE),
            ]
        ]
        expected = {row.pk: row.date_range for row in other_rows}
        self.migrate(LATEST)
        seeded.refresh_from_db()
        self.assertEqual(seeded.date_range, self.dates.NEW_DATE_RANGE)
        for row in other_rows:
            row.refresh_from_db()
            self.assertEqual(row.date_range, expected[row.pk])
        self.migrate(SEED)
        seeded.refresh_from_db()
        self.assertEqual(seeded.date_range, self.dates.OLD_DATE_RANGE)
        for row in other_rows:
            row.refresh_from_db()
            self.assertEqual(row.date_range, expected[row.pk])

    def test_reverse_and_migrate_to_latest_again(self):
        self.migrate(LATEST)
        self.migrate(BEFORE_SEED)
        apps = self.migrate(LATEST)
        Job = apps.get_model('jobs', 'Job')
        Project = apps.get_model('jobs', 'Project')
        self.assertEqual(Job.objects.count(), 3)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Job.objects.get(company='IBM').date_range, self.dates.NEW_DATE_RANGE)
        for job in Job.objects.exclude(logo=''):
            self.assertTrue(job.logo.storage.exists(job.logo.name))
