"""
Module used to test the
business/email/low_budget_notification/notify_low_available_amount method,
used to notify when the budget amount is less or equal than the configure
'low' amount.
"""
from budget.business.email.low_budget_notification import (
    notify_low_available_amount)
from django.test import TestCase
from budget.models.budget import Budget
from unittest.mock import patch


class NotifyLowAvailableAmountTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/budget',
    ]

    @patch('budget.business.email.low_budget_notification.send_email')
    def test_notify_low_available_amount(self, mocked_send_email):
        b = Budget.objects.get(pk=8)

        notify_low_available_amount(b)

        assert mocked_send_email.called_once
