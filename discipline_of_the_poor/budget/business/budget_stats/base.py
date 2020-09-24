"""
Module used to define the base functions needed for the suite to get a
budget's stats information
"""
import importlib


def get_budget_stats(user, budget):
    """
    Function used to fetch a customer's budget stats according to its privilege
    :param DotpUser user: the logged in user
    :param Budget budget: The budget object instance
    :return dict: The requested budget's stats information
    """
    user_privilege = user.privilege

    module = importlib.import_module(
        'budget.business.budget_stats.' + user_privilege)

    budget_stats_handler = getattr(module, 'get_budget_stats')

    result = budget_stats_handler(user, budget)

    return result
