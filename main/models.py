from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Account(User):
    pass

class Profile(models.Model):
    pass