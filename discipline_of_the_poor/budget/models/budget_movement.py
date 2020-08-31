"""
Module for the BudgetMovement model, used to store all the movements
performed on a budget
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.budget import Budget
from budget.models.movement import Movement
import reversion


@reversion.register()
class BudgetMovement(BaseMixin):
    budget = models.ForeignKey(Budget, on_delete=models.DO_NOTHING)
    movement = models.ForeignKey(Movement, on_delete=models.DO_NOTHING)
    # direction true to add to the budget, false for otherwise
    direction = models.BooleanField()

    def save(self, *args, **kwargs):
        """
        Method used to alter the budget's available amount.
        """
        if self.active:
            budget = self.budget
            amount = self.movement.amount

            if self.direction:
                budget.available_amount = budget.available_amount + amount
            else:
                budget.available_amount = budget.available_amount - amount

            budget.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Method used to alter the budget's available amount. On deletion
        reverse the actions made on creation
        """
        budget = self.budget
        amount = self.movement.amount

        if self.direction:
            budget.available_amount = budget.available_amount - amount
        else:
            budget.available_amount = budget.available_amount + amount

        budget.save()
        super().delete(*args, **kwargs)
