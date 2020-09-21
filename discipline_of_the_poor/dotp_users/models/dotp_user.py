"""
Module used to handle custom app users
"""
from django.contrib.auth.models import AbstractUser
from guardian.mixins import GuardianUserMixin
from django.db import models
from django.utils.translation import gettext as _


class DotpUser(AbstractUser, GuardianUserMixin):
    PREMIUM = 'premium'
    REGULAR = 'regular'
    PRIVILEGE_CHOICES = [
        (PREMIUM, _('Premium customer')),
        (REGULAR, _('Regular customer')),
    ]
    privilege = models.CharField(
        max_length=10,
        choices=PRIVILEGE_CHOICES,
        default=REGULAR,
    )
