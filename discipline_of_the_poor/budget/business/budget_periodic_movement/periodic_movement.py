"""
Module used to provide a function that creates a charge (BudgetMovement)
based on a periodic movement's time.
"""
from budget.models.periodic_movement import PeriodicMovement
from budget.models.budget_movement import BudgetMovement


def charge_periodic_movement(movement_id):
    """
    Function used to create a charge related to a PeriodicMovement time to
    perform the operation
    :param str movement_id: id of the PeriodicMovement to charge
    :return: 
    """
    periodic_movement = PeriodicMovement.objects.get(id=movement_id)

    category = periodic_movement.movement.category.unique_name
    direction = True if category == 'income' else False

    budget_movement_data = {
        'budget': periodic_movement.budget,
        'movement': periodic_movement.movement,
        'direction': direction,
        'owner': periodic_movement.owner,
    }

    charge = BudgetMovement.objects.create(**budget_movement_data)

    return charge
