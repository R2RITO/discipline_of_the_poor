"""
Module for the BudgetMovement model, used to store all the movements
performed on a budget
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.budget import Budget
from budget.models.movement import Movement
from dotp_users.models.mixins import OwnershipMixin
import reversion
from budget.business.email.low_budget_notification import (
    notify_low_available_amount)


@reversion.register()
class BudgetMovement(BaseMixin, OwnershipMixin):
    budget = models.ForeignKey(Budget, on_delete=models.DO_NOTHING)
    movement = models.ForeignKey(Movement, on_delete=models.DO_NOTHING)
    # direction true to add to the budget, false for otherwise
    direction = models.BooleanField()

    def save(self, *args, **kwargs):
        """
        Method used to alter the budget's available amount.
        """
        if not self.hidden:
            budget = self.budget
            amount = self.movement.amount

            if self.direction:
                budget.available_amount = budget.available_amount + amount
            else:
                budget.available_amount = budget.available_amount - amount

            budget.save()

            if (budget.owner.notify_low_budget_amount and
                    budget.available_amount < budget.low_amount):
                notify_low_available_amount(budget)

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

        if (budget.owner.notify_low_budget_amount and
                budget.available_amount < budget.low_amount):
            notify_low_available_amount(budget)

        super().delete(*args, **kwargs)
