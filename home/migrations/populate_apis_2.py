# Generated by Django 3.0.1 on 2020-03-20 04:47

import sys
from django.db import migrations


def load_apis(apps, schema_editor):
    Api = apps.get_model('home', 'Api')
    api_fantasy_epl = Api(id=0, name="Fantasy EPL", request_limit_type_id=0, request_interval_ms=10000)
    api_fantasy_epl.save()

    api_football_data_dot_org = Api(id=1, name="football-data.org", request_limit_type_id=0, request_interval_ms=10000)
    api_football_data_dot_org.save()


def delete_apis(apps, schema_editor):
    Api = apps.get_model('home', 'Api')
    Api.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', 'populate_request_limit_type'),
    ]

    operations = [
        migrations.RunPython(load_apis, delete_apis)
    ] if 'test' not in sys.argv[1:] else []
