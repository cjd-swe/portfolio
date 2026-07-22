from django.db import migrations


OLD_DATE_RANGE = 'Feb 2024 – Dec 2025'
NEW_DATE_RANGE = 'Aug 2021 – Dec 2025'


def update_ibm_date_range(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    Job.objects.filter(company='IBM').update(date_range=NEW_DATE_RANGE)


def restore_ibm_date_range(apps, schema_editor):
    Job = apps.get_model('jobs', 'Job')
    Job.objects.filter(company='IBM').update(date_range=OLD_DATE_RANGE)


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_seed_experience_and_projects'),
    ]

    operations = [
        migrations.RunPython(update_ibm_date_range, restore_ibm_date_range),
    ]
