from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_name)
