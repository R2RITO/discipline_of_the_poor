"""
Module used to test the
business/budget_stats/*/get_budget_stats methods
which are responsible for retrieving the budget stats based on a customer's
privilege
"""
from budget.business.budget_stats.base import (
    get_budget_stats as get_budget_stats_base)
from budget.business.budget_stats.premium import (
    get_budget_stats as get_budget_stats_premium)
from budget.business.budget_stats.regular import (
    get_budget_stats as get_budget_stats_regular)
from django.test import TestCase
from budget.models.budget import Budget
from dotp_users.models.dotp_user import DotpUser
from django.utils import translation


class GetBudgetStatsTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/budget',
    ]

    def test_get_premium_stats_default_language(self):
        b = Budget.objects.get(pk=8)
        user = DotpUser.objects.get(pk=4)

        stats = get_budget_stats_base(user, b)

        assert 'message' in stats
        assert stats.get('message') == "Congratulations premium user!"

    def test_get_premium_stats_spanish(self):
        b = Budget.objects.get(pk=8)
        user = DotpUser.objects.get(pk=4)

        with translation.override('es'):
            stats = get_budget_stats_base(user, b)

        assert 'message' in stats
        assert stats.get('message') == "¡Felicitaciones usuario premium!"

    def test_get_regular_stats(self):
        b = Budget.objects.get(pk=8)
        user = DotpUser.objects.get(pk=3)

        stats = get_budget_stats_base(user, b)

        assert not stats


class GetBudgetStatsPremiumTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/budget',
    ]

    def test_get_stats_default_language(self):
        b = Budget.objects.get(pk=8)
        user = DotpUser.objects.get(pk=4)

        stats = get_budget_stats_premium(user, b)

        assert 'message' in stats
        assert stats.get('message') == "Congratulations premium user!"

    def test_get_stats_spanish(self):
        b = Budget.objects.get(pk=8)
        user = DotpUser.objects.get(pk=4)

        with translation.override('es'):
            stats = get_budget_stats_premium(user, b)

        assert 'message' in stats
        assert stats.get('message') == "¡Felicitaciones usuario premium!"


class GetBudgetStatsRegularTest(TestCase):

    fixtures = [
        'budget/tests/fixtures/dotp_user',
        'budget/tests/fixtures/budget',
    ]

    def test_get_stats(self):
        b = Budget.objects.get(pk=8)
        user = DotpUser.objects.get(pk=3)

        stats = get_budget_stats_regular(user, b)

        assert not stats
