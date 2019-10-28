from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Account(AbstractUser):
    date_born = models.DateField(null=True)

    def __str__(self):
        return self.account.username


class Profile(models.Model):
    bio = models.TextField(max_length=200)
    account = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.account.username


class Friend(models.Model):
    profiles = models.ManyToManyField(Profile)
