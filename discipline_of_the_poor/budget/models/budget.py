"""
Module for the Budget model, used to store all the budgets of a user with their
available amounts
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.movement import Movement
from dotp_users.models.mixins import OwnershipMixin
import reversion


@reversion.register()
class Budget(BaseMixin, OwnershipMixin):
    unique_name = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    available_amount = models.FloatField()
    movements = models.ManyToManyField(
        Movement,
        through='BudgetMovement',
        related_name='budgets',
    )
