# Generated by Django 4.2.7 on 2023-11-19 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interest',
            name='created_by',
        ),
    ]
