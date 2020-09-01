"""
Module used to handle custom app users
"""
from django.contrib.auth.models import AbstractUser
#from guardian.mixins import GuardianUserMixin


class DotpUser(AbstractUser):#, GuardianUserMixin):
    pass
