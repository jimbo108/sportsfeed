# Generated by Django 3.0.1 on 2019-12-31 09:54

from django.db import migrations

def load_teams(apps, schema_editor):
    pass

def delete_teams(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_teams, delete_teams)
    ]
