from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    SEXES = [
        ('male', 'Мужской'),
        ('female', 'Женский')
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    about = models.TextField(blank=True)
    birthday = models.DateField()
    avatar_path = models.URLField(null=True)
    rate = models.FloatField(default=0.0)
    sex = models.CharField(max_length=7, choices=SEXES)
    is_organizer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ActivationCode(models.Model):
    code = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
