"""
Module used to store various useful mixins related to the users
"""
from django.db import models
from django.conf import settings


class OwnershipMixin(models.Model):
    """
    Base class used to provide ownership attribute
    """
    class Meta:
        abstract = True

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
