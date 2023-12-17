from django.db import models

from interest.models import Interest
from user_profile.models import UserProfile


class InterestGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    interests = models.ManyToManyField(Interest)
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    participants = models.ManyToManyField(UserProfile, through='InterestGroupParticipant',
                                          related_name='participant_interest_group')
    max_num_participants = models.IntegerField(default=0)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class InterestGroupParticipant(models.Model):
    interest_group = models.ForeignKey(InterestGroup, on_delete=models.CASCADE)
    participant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    num_warns = models.IntegerField(default=0)
    is_banned = models.BooleanField(default=False)

    class Meta:
        unique_together = ('interest_group', 'participant')
