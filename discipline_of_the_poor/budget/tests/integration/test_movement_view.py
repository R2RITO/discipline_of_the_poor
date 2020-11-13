"""
Module used to test the Movement view, with all the available
operations
"""
from django.test import TestCase
from django.urls import reverse


class MovementViewTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/movement_category',
        'budget/tests/fixtures/movement',
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

    def test_get_all_movements(self):

        result = self.client.get(
            reverse('movement-list'),
            HTTP_AUTHORIZATION=self.auth_header
        )
        movements = result.json()

        assert len(movements) == 7
