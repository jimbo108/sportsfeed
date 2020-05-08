# Generated by Django 3.0.1 on 2020-04-25 05:48

import sys
from django.db import migrations

def load_fixture_status_mappings(apps, schema_editor):
    FixtureStatusMapping = apps.get_model('home', 'FixtureStatusMapping')
     
    FixtureStatusMapping(id=0, value_id=0, api_id=1, string_external_identifier='FINISHED').save()

    FixtureStatusMapping(id=1, value_id=1, api_id=1,
                         string_external_identifier='IN_PLAY').save()

    FixtureStatusMapping(id=2, value_id=2, api_id=1, string_external_identifier='PAUSED').save()

    FixtureStatusMapping(id=3, value_id=3, api_id=1,
                         string_external_identifier='POSTPONED').save()

    FixtureStatusMapping(id=4, value_id=4, api_id=1,
                         string_external_identifier='SCHEDULED').save()

    FixtureStatusMapping(id=5, value_id=5, api_id=1,
                         string_external_identifier='SUSPENDED').save()

    FixtureStatusMapping(id=6, value_id=6, api_id=1,
                         string_external_identifier='AWARDED').save()

    FixtureStatusMapping(id=7, value_id=7, api_id=1,
                         string_external_identifier='CANCELED').save()

    
def delete_fixture_status_mappings(apps, schema_editor):
    FixtureStatusMapping = apps.get_model('home', 'FixtureStatusMapping')
    FixtureStatusMapping.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', 'populate_fixture_statuses'),
    ]

    operations = [
        migrations.RunPython(load_fixture_status_mappings, delete_fixture_status_mappings)
    ] if 'test' not in sys.argv[1:] else []