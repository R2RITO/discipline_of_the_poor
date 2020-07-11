"""
Module for the Movement model, used to store all the movements created by the
users
"""
from django.db import models
from budget.models.mixins import BaseMixin


class Movement(BaseMixin):
    unique_name = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    amount = models.FloatField()
