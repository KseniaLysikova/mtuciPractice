# Generated by Django 5.0.6 on 2024-07-01 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_job_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='url',
        ),
    ]
