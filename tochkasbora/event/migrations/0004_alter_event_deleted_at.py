# Generated by Django 4.2.7 on 2023-11-19 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_banner_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
