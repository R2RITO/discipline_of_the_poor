"""
Module used to test the Budget view, with all the available
operations
"""
from django.test import TestCase
from django.urls import reverse
from dotp_users.models.dotp_user import DotpUser


class BudgetViewTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
    ]

    def setUp(self) -> None:

        # Auth setup
        auth_credentials = {
            'username': 'arturo',
            'password': 'arturo',
        }
        auth_result = self.client.post(
            reverse('token_obtain_pair'),
            data=auth_credentials
        )

        self.auth_header = 'Bearer ' + auth_result.json().get('access')

    def test_activate_notify_low_budget_amount(self):
        params = {
            'notify': True,
        }
        result = self.client.post(
            reverse('notifylowbudgetamount-list'),
            HTTP_AUTHORIZATION=self.auth_header,
            content_type='application/json',
            data=params
        )

        user = DotpUser.objects.get(pk=4)

        assert result.json().get('notify') is True
        assert result.status_code == 200
        assert user.notify_low_budget_amount is True
