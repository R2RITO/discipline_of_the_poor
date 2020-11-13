"""
Module used to test the SingleMovement view, with all the available
operations
"""
from django.test import TestCase
from django.urls import reverse
from budget.models.budget import Budget
from budget.models.single_movement import SingleMovement
from dotp_users.models.dotp_user import DotpUser


class SingleMovementViewTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/budget',
        'budget/tests/fixtures/movement_category',
        'budget/tests/fixtures/movement',
        'budget/tests/fixtures/single_movement',
        'budget/tests/fixtures/budget_movement',
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

    def test_get_all_single_movements(self):

        result = self.client.get(
            reverse('singlemovement-list'),
            HTTP_AUTHORIZATION=self.auth_header
        )
        s_movements = result.json()

        # Only two movements that this owner can see
        assert len(s_movements) == 2
        assert result.status_code == 200

    def test_retrieve_owned_single_movement(self):

        result = self.client.get(
            reverse('singlemovement-detail', kwargs={'pk': 39}),
            HTTP_AUTHORIZATION=self.auth_header
        )
        movement_obj = result.json()

        assert movement_obj.get('movement').get('id') == 39
        assert result.status_code == 200

    def test_retrieve_someone_elses_single_movement(self):

        result = self.client.get(
            reverse('budget-detail', kwargs={'pk': 24}),
            HTTP_AUTHORIZATION=self.auth_header
        )
        sm = SingleMovement.objects.get(pk=24)
        usr = DotpUser.objects.get(username='arturo')

        assert sm.owner.id != usr.id
        assert result.status_code == 404

    def test_create_single_movement_income(self):

        # Budget used
        budget_obj = Budget.objects.get(pk=7)
        previous_amount = budget_obj.available_amount

        params = {
            "movement": {
                "description": "Test single movement income",
                "amount": 50.0,
                "category": 1
            },
            "budget": 7
        }
        result = self.client.post(
            reverse('singlemovement-list'),
            HTTP_AUTHORIZATION=self.auth_header,
            content_type='application/json',
            data=params
        )

        # Raises SingleMovement.DoesNotExist on error
        created_sm = SingleMovement.objects.get(
            movement__description="Test single movement income")

        # Check budget's updated amount
        budget_obj.refresh_from_db()
        assert (
            budget_obj.available_amount ==
            previous_amount + created_sm.movement.amount
        )

        assert created_sm
        assert result.status_code == 201

    def test_create_single_movement_expense(self):

        # Budget used
        budget_obj = Budget.objects.get(pk=8)
        previous_amount = budget_obj.available_amount

        params = {
            "movement": {
                "description": "Test single movement expense",
                "amount": 50.0,
                "category": 2
            },
            "budget": 8
        }
        result = self.client.post(
            reverse('singlemovement-list'),
            HTTP_AUTHORIZATION=self.auth_header,
            content_type='application/json',
            data=params
        )

        # Raises SingleMovement.DoesNotExist on error
        created_sm = SingleMovement.objects.get(
            movement__description="Test single movement expense")

        # Check budget's updated amount
        budget_obj.refresh_from_db()
        assert (
            budget_obj.available_amount ==
            previous_amount - created_sm.movement.amount
        )

        assert created_sm
        assert result.status_code == 201

    def test_create_single_movement_missing_required_fields(self):
        params = {
            'budget': 10,
        }
        result = self.client.post(
            reverse('singlemovement-list'),
            HTTP_AUTHORIZATION=self.auth_header,
            content_type='application/json',
            data=params
        )

        assert result.status_code == 400

    def test_update_single_movement_change_budget(self):
        """
        This test changes the budget of a registered single income movement,
        thus, the old budget should lose the added amount and the new budget
        should receive the added amount.
        :return:
        """
        old_b = Budget.objects.get(pk=8)
        new_b = Budget.objects.get(pk=7)
        sm = SingleMovement.objects.get(pk=39)
        old_b_amount = old_b.available_amount
        new_b_amount = new_b.available_amount
        sm_amount = sm.movement.amount

        params = {
            'budget': 7,
        }
        result = self.client.patch(
            reverse('singlemovement-detail', kwargs={'pk': 39}),
            HTTP_AUTHORIZATION=self.auth_header,
            data=params,
            content_type='application/json'
        )

        old_b.refresh_from_db()
        new_b.refresh_from_db()

        assert old_b.available_amount == old_b_amount - sm_amount
        assert new_b.available_amount == new_b_amount + sm_amount
        assert result.status_code == 200

    def test_update_non_existing_single_movement(self):
        params = {
            'budget': 7,
        }
        result = self.client.patch(
            reverse('singlemovement-detail', kwargs={'pk': 42}),
            HTTP_AUTHORIZATION=self.auth_header,
            data=params,
            content_type='application/json'
        )
        assert result.status_code == 404

    def test_update_someone_elses_single_movement(self):
        params = {
            'budget': 7,
        }
        result = self.client.patch(
            reverse('singlemovement-detail', kwargs={'pk': 26}),
            HTTP_AUTHORIZATION=self.auth_header,
            data=params,
            content_type='application/json'
        )
        sm = SingleMovement.objects.get(pk=26)
        usr = DotpUser.objects.get(username='arturo')

        assert sm.owner.id != usr.id
        assert result.status_code == 404

    # def test_update_single_movement_with_someone_elses_budget(self):
    #     params = {
    #         'budget': 3,
    #     }
    #     result = self.client.patch(
    #         reverse('singlemovement-detail', kwargs={'pk': 39}),
    #         HTTP_AUTHORIZATION=self.auth_header,
    #         data=params,
    #         content_type='application/json'
    #     )
    #     b = Budget.objects.get(pk=3)
    #     usr = DotpUser.objects.get(username='arturo')
    #
    #     assert b.owner.id != usr.id
    #     assert result.status_code == 404

    def test_delete_single_movement(self):
        """
        This test deletes a single movement, thus reversing the operation made
        when creating it. Since this is an income movement, the budget should
        have the amount subtracted from its available amount
        :return:
        """
        b = Budget.objects.get(pk=8)
        sm = SingleMovement.objects.get(pk=39)
        b_amount = b.available_amount
        sm_amount = sm.movement.amount

        result = self.client.delete(
            reverse('singlemovement-detail', kwargs={'pk': 39}),
            HTTP_AUTHORIZATION=self.auth_header,
        )
        b.refresh_from_db()
        sm.refresh_from_db()

        assert b.available_amount == b_amount - sm_amount
        assert sm.hidden
        assert result.status_code == 204

    def test_delete_non_existing_single_movement(self):
        result = self.client.delete(
            reverse('singlemovement-detail', kwargs={'pk': 42}),
            HTTP_AUTHORIZATION=self.auth_header,
        )

        assert result.status_code == 404

    def test_delete_someone_elses_single_amount(self):
        result = self.client.delete(
            reverse('budget-detail', kwargs={'pk': 26}),
            HTTP_AUTHORIZATION=self.auth_header,
        )

        assert result.status_code == 404
