# Generated by Django 4.2.7 on 2023-11-19 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_remove_event_datetime_creation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='organizer',
            new_name='organizer_id',
        ),
    ]
