# Generated by Django 4.2.7 on 2023-11-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_created_at_event_deleted_at_event_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='banner_url',
            field=models.URLField(null=True),
        ),
    ]
