# Generated by Django 4.1.2 on 2023-04-12 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0002_remove_application_target_application_domain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='method',
            field=models.CharField(choices=[('HEAD', 'HEAD'), ('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('DELETE', 'DELETE'), ('OPTIONS', 'OPTIONS'), ('TRACE', 'TRACE'), ('CONNECT', 'CONNECT')], default='GET', max_length=8),
        ),
        migrations.AlterField(
            model_name='code',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='codes', to='flow.application'),
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='application',
            field=models.ForeignKey(help_text="Endpoint's application", on_delete=django.db.models.deletion.RESTRICT, related_name='endpoints', to='flow.application'),
        ),
    ]
