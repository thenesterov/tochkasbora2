# Generated by Django 4.2.7 on 2023-12-12 08:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interest_group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interestgroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interestgroup',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interestgroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
