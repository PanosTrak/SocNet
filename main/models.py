from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Account(AbstractUser):
    date_born = models.DateField(null=True)


class Profile(models.Model):
    bio = models.TextField(max_length=200)
    account = models.OneToOneField(
        to=Account, on_delete=models.SET_NULL, null=True)


class FriendList(models.Model):
    account_1 = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='account_1')
    account_2 = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='account_2')
