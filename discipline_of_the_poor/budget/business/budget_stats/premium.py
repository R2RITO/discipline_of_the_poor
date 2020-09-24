"""
Module used to define a function to get the budget's stats for a premium
customer
"""
from django.utils.translation import gettext as _


def get_budget_stats(user, budget):
    """
    Function used to fetch a customer's budget stats according to its privilege
    :param DotpUser user: the logged in user
    :param Budget budget: The budget object instance
    :return dict: The requested budget's stats information
    """
    stats = {}

    # Add message
    stats['message'] = _("Congratulations premium user!")

    return stats
