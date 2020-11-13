"""
Module used to test the Budget view, with all the available
operations
"""
from django.test import TestCase
from django.urls import reverse
from budget.models.budget import Budget
from dotp_users.models.dotp_user import DotpUser
from django.conf import settings


class BudgetViewTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/budget',
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

        # Photo setup
        self.photo_path = settings.BASE_DIR / 'budget/tests/fixtures/avatar.png'

    def test_get_all_budgets(self):

        result = self.client.get(
            reverse('budget-list'),
            HTTP_AUTHORIZATION=self.auth_header
        )
        budgets = result.json()

        # Only two budgets that this owner can see
        assert len(budgets) == 2
        assert result.status_code == 200

    def test_retrieve_owned_budget(self):

        result = self.client.get(
            reverse('budget-detail', kwargs={'pk': 7}),
            HTTP_AUTHORIZATION=self.auth_header
        )
        budget_obj = result.json()

        assert budget_obj.get('id') == 7
        assert result.status_code == 200

    def test_retrieve_someone_elses_budget(self):

        result = self.client.get(
            reverse('budget-detail', kwargs={'pk': 4}),
            HTTP_AUTHORIZATION=self.auth_header
        )
        b = Budget.objects.get(pk=4)
        usr = DotpUser.objects.get(username='arturo')

        assert b.owner.id != usr.id
        assert result.status_code == 404

    def test_create_budget(self):

        with open(self.photo_path, 'rb') as p:
            params = {
                'unique_name': 'test_budget',
                'description': 'Test description',
                'photo': p,
            }
            result = self.client.post(
                reverse('budget-list'),
                HTTP_AUTHORIZATION=self.auth_header,
                data=params
            )

        # Raises Budget.DoesNotExist on error
        created_budget = Budget.objects.get(unique_name='test_budget')

        assert created_budget
        assert result.status_code == 201

    def test_create_existing_budget(self):
        with open(self.photo_path, 'rb') as p:
            params = {
                'unique_name': 'photo_budget',
                'description': 'Test description',
                'photo': p,
            }
            result = self.client.post(
                reverse('budget-list'),
                HTTP_AUTHORIZATION=self.auth_header,
                data=params
            )

        assert result.status_code == 400

    def test_create_budget_missing_required_fields(self):
        params = {
            'description': 'Test description',
        }
        result = self.client.post(
            reverse('budget-list'),
            HTTP_AUTHORIZATION=self.auth_header,
            content_type='application/json',
            data=params
        )

        assert result.status_code == 400

    def test_update_budget(self):
        params = {
            'description': 'Test updated',
        }
        result = self.client.patch(
            reverse('budget-detail', kwargs={'pk': 7}),
            HTTP_AUTHORIZATION=self.auth_header,
            data=params,
            content_type='application/json'
        )
        assert result.status_code == 200

    def test_update_non_existing_budget(self):
        params = {
            'description': 'Test updated',
        }
        result = self.client.patch(
            reverse('budget-detail', kwargs={'pk': 41}),
            HTTP_AUTHORIZATION=self.auth_header,
            data=params,
            content_type='application/json'
        )
        assert result.status_code == 404

    def test_update_someone_elses_budget(self):
        params = {
            'description': 'Test updated',
        }
        result = self.client.patch(
            reverse('budget-detail', kwargs={'pk': 4}),
            HTTP_AUTHORIZATION=self.auth_header,
            data=params,
            content_type='application/json'
        )
        b = Budget.objects.get(pk=4)
        usr = DotpUser.objects.get(username='arturo')

        assert b.owner.id != usr.id
        assert result.status_code == 404

    def test_delete_budget(self):
        result = self.client.delete(
            reverse('budget-detail', kwargs={'pk': 7}),
            HTTP_AUTHORIZATION=self.auth_header,
        )
        b = Budget.all_objects.get(pk=7)

        assert b.hidden
        assert result.status_code == 204

    def test_delete_non_existing_budget(self):
        result = self.client.delete(
            reverse('budget-detail', kwargs={'pk': 42}),
            HTTP_AUTHORIZATION=self.auth_header,
        )

        assert result.status_code == 404

    def test_delete_someone_elses_budget(self):
        result = self.client.delete(
            reverse('budget-detail', kwargs={'pk': 4}),
            HTTP_AUTHORIZATION=self.auth_header,
        )

        assert result.status_code == 404
