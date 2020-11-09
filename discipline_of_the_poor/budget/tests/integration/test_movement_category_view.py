"""
Module used to test the MovementCategory view, with all the available
operations
"""
from django.test import TestCase
from django.urls import reverse


class MovementCategoryViewTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/movement_category',
    ]

    def test_get_all_categories_default_language(self):

        result = self.client.get(reverse('movementcategory-list'))
        mcs = result.json()

        income_mc = [mc for mc in mcs if mc.get('unique_name') == 'income'][0]
        expense_mc = [mc for mc in mcs if mc.get('unique_name') == 'expense'][0]

        assert len(mcs) == 2
        assert income_mc.get(
            'description') == "Income movement, adds to the budget"
        assert expense_mc.get(
            'description') == "Expense movement, substracts from the budget"

    def test_get_all_categories_spanish(self):

        result = self.client.get(
            reverse('movementcategory-list'),
            HTTP_ACCEPT_LANGUAGE='es',
        )
        mcs = result.json()

        income_mc = [mc for mc in mcs if mc.get('unique_name') == 'income'][0]
        expense_mc = [mc for mc in mcs if mc.get('unique_name') == 'expense'][0]

        assert len(mcs) == 2
        assert income_mc.get(
            'description') == "Movimiento de ingreso, agrega al presupuesto"
        assert expense_mc.get(
            'description') == "Movimiento de egreso, sustrae del presupuesto"

