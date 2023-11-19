from django.db import models

from interest.models import Interest
from user_profile.models import UserProfile


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    is_open = models.BooleanField(default=True)
    max_num_participants = models.IntegerField(default=0)
    datetime_event = models.DateTimeField()
    organizer_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='organizer_event')
    rate = models.FloatField(default=0.0)
    address = models.CharField(max_length=512)
    interests = models.ManyToManyField(Interest)
    participants = models.ManyToManyField(UserProfile, through='EventParticipant', related_name='participant_event')
    banner_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class EventParticipant(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    num_warns = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event_id', 'participant_id')
