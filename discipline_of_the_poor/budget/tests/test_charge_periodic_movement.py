"""
Module used to test the
business/budget_periodic_movement/periodic_movement/charge_periodic_movement
method, that is responsible for updating a budget when the period arrives
"""
from budget.business.budget_periodic_movement.periodic_movement import (
    charge_periodic_movement)
from django.test import TestCase
from budget.models.budget import Budget
from budget.models.periodic_movement import PeriodicMovement


class ChargePeriodicMovementTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/movement_category',
        'budget/tests/fixtures/budget',
        'budget/tests/fixtures/movement',
        'budget/tests/fixtures/periodic_movement',
    ]

    def test_add_to_budget(self):
        b = Budget.objects.get(pk=8)
        mv = PeriodicMovement.objects.get(pk=38)
        expected_amount = b.available_amount + mv.amount

        charge_periodic_movement(38)
        b.refresh_from_db()

        assert expected_amount == b.available_amount

