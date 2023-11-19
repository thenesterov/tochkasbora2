from django.contrib.auth.models import User
from django.db import models


class Interest(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
