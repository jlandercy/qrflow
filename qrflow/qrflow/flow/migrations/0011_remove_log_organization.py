# Generated by Django 4.1.2 on 2023-10-01 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0010_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='organization',
        ),
    ]
