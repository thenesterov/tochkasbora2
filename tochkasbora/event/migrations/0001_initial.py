# Generated by Django 4.2.7 on 2023-11-19 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0003_userprofile_interests'),
        ('interest', '0002_remove_interest_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1024)),
                ('is_open', models.BooleanField(default=True)),
                ('max_num_participants', models.IntegerField(default=0)),
                ('datetime_event', models.DateTimeField()),
                ('datetime_creation', models.DateTimeField()),
                ('rate', models.FloatField(default=0.0)),
                ('address', models.CharField(max_length=512)),
                ('interests', models.ManyToManyField(to='interest.interest')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizer_event', to='user_profile.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_warns', models.IntegerField(default=0)),
                ('is_banned', models.BooleanField(default=False)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('participant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.userprofile')),
            ],
            options={
                'unique_together': {('event_id', 'participant_id')},
            },
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='participant_event', through='event.EventParticipant', to='user_profile.userprofile'),
        ),
    ]
