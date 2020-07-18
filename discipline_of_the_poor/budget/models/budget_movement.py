"""
Module for the BudgetMovement model, used to store all the movements
performed on a budget
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.budget import Budget
from budget.models.movement import Movement


class BudgetMovement(BaseMixin):
    budget = models.ForeignKey(Budget, on_delete=models.DO_NOTHING)
    movement = models.ForeignKey(Movement, on_delete=models.DO_NOTHING)
    # direction true to add to the budget, false for otherwise
    direction = models.BooleanField()
