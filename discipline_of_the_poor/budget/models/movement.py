"""
Module for the Movement model, used to store all the movements created by the
users
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.movement_category import MovementCategory
from dotp_users.models.mixins import OwnershipMixin


class Movement(BaseMixin, OwnershipMixin):
    description = models.TextField()
    amount = models.FloatField()
    category = models.ForeignKey(MovementCategory, on_delete=models.DO_NOTHING)
