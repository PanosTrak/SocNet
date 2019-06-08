from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Account(User):
    date_born = models.DateField(null=True)