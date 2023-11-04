from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(max_length=120, unique=True, null=True)
    email = models.EmailField(_("email address"), unique=True)

    subscribers = models.IntegerField(default=0)

    def __str__(self):
        return self.username
