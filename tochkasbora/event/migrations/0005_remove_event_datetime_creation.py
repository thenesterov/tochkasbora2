# Generated by Django 4.2.7 on 2023-11-19 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_deleted_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='datetime_creation',
        ),
    ]
