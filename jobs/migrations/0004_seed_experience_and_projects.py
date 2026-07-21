import os

from django.conf import settings
from django.core.files import File
from django.db import migrations


JOBS = [
    dict(
        title='Forward Deployed Engineer',
        company='Artium AI',
        date_range='Mar 2026 – Present',
        description=(
            'Embed directly with clients to design, build, and ship secure, scalable '
            'backend and cloud infrastructure — writing Go, running Kubernetes, and '
            'building out the CI/CD pipelines that get it all to production.'
        ),
        order=0,
        logo_filename='artium_logo.png',
    ),
    dict(
        title='Software Engineer',
        company='IBM',
        date_range='Feb 2024 – Dec 2025',
        description=(
            'Built an internal AI-powered cloud assistant and delivered a security and '
            'compliance tooling platform that reduced reporting overhead for engineers '
            'and improved audit readiness for client environments.'
        ),
        order=1,
        logo_filename='ibm_logo.svg',
    ),
    dict(
        title='Owner / Technician',
        company='CAMUVA Mobile',
        date_range='2017 – 2022',
        description=(
            'Self-started business offering iPhone repair services, including screen '
            'repair and battery replacement.'
        ),
        order=2,
        logo_filename=None,
    ),
]

PROJECTS = [
    dict(
        name='SharpWatch (CAPFREE)',
        description=(
            'A sports-picks tracker that ingests picks from screenshots or manual entry, '
            'auto-grades bets against live-score providers, and exposes a Next.js '
            'dashboard for analytics. FastAPI backend with OCR/vision-assisted parsing, '
            'Postgres storage, deployed on Render + Vercel.'
        ),
        url='https://github.com/cjd-swe/CAPFREE',
        order=0,
    ),
    dict(
        name='Spotify Mood Ring',
        description=(
            'A mobile PWA that reads your Spotify listening history and generates a '
            'shareable AI-powered mood report.'
        ),
        url='https://github.com/cjd-swe/spotify-mood-ring',
        order=1,
    ),
]

LOGO_DIR = os.path.join(settings.BASE_DIR, 'jobs', 'static', 'job_logos')


def seed_data(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    Project = apps.get_model('jobs', 'Project')

    for job_data in JOBS:
        logo_filename = job_data.pop('logo_filename')
        job, created = Job.objects.get_or_create(
            title=job_data['title'], company=job_data['company'], defaults=job_data,
        )
        if created and logo_filename:
            logo_path = os.path.join(LOGO_DIR, logo_filename)
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    job.logo.save(logo_filename, File(f), save=True)

    for project_data in PROJECTS:
        Project.objects.get_or_create(name=project_data['name'], defaults=project_data)


def remove_data(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    Project = apps.get_model('jobs', 'Project')
    Job.objects.filter(company__in=['Artium AI', 'IBM', 'CAMUVA Mobile']).delete()
    Project.objects.filter(name__in=['SharpWatch (CAPFREE)', 'Spotify Mood Ring']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_project_skill_alter_job_options_remove_job_image_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_data),
    ]
