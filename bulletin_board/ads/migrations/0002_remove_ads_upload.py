# Generated by Django 4.2.18 on 2025-01-19 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ads',
            name='upload',
        ),
    ]
