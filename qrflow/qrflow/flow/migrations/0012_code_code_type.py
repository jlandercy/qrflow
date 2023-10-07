# Generated by Django 4.1.2 on 2023-10-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0011_remove_log_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='code_type',
            field=models.CharField(choices=[('EAN13', 'EAN13'), ('QR', 'QR'), ('QR-EPC', 'QR-EPC'), ('QR-DGC', 'QR-DGC')], default='QR', help_text='Type of code', max_length=8),
        ),
    ]