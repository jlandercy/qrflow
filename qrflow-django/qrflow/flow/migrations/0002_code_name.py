# Generated by Django 4.1.2 on 2022-11-12 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='name',
            field=models.CharField(default='', max_length=1024, unique=True),
            preserve_default=False,
        ),
    ]
