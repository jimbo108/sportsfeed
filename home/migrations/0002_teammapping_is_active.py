# Generated by Django 3.0.1 on 2020-01-05 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_auto_20200104_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammapping',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
