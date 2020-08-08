"""
Module for the Movement model, used to store all the movements created by the
users
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.movement_category import MovementCategory


class Movement(BaseMixin):
    description = models.TextField()
    amount = models.FloatField()
    category = models.ForeignKey(MovementCategory, on_delete=models.DO_NOTHING)
