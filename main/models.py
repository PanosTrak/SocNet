from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Account(User):
    date_born = models.DateField(null=True)

class Profile(models.Model):
    uid = models.IntegerField(primary_key=True)
    account_id = models.OneToOneField(Account, on_delete=models.SET_NULL, null=True)
    picture = models.ImageField()
    bio = models.TextField()