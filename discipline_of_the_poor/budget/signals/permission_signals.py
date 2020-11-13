"""
Module used to define functions to handle django signals, in order to
further customize model storage
"""

from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Permission
from django.dispatch import receiver

from dotp_users.models.mixins import OwnershipMixin

from budget.models.budget import Budget
from budget.models.budget_movement import BudgetMovement
from budget.models.movement import Movement
from budget.models.periodic_movement import PeriodicMovement
from budget.models.single_movement import SingleMovement
from budget.models.movement_category import MovementCategory


MODEL_CLASSES_PERMS = {
    Budget.__name__.lower(): ['add', 'change', 'view', 'delete'],
    BudgetMovement.__name__.lower(): ['add', 'change', 'view', 'delete'],
    Movement.__name__.lower(): ['add', 'change', 'view', 'delete'],
    PeriodicMovement.__name__.lower(): ['add', 'change', 'view', 'delete'],
    SingleMovement.__name__.lower(): ['add', 'change', 'view', 'delete'],
    MovementCategory.__name__.lower(): ['view'],
}


@receiver(post_save)
def owner_permissions(sender, **kwargs):
    """
    Function used to assign read and write permissions to the owner
    of the model created
    """
    if kwargs.get('raw', False):
        model_obj = sender.objects.get(pk=kwargs['instance'].pk)
    else:
        model_obj = kwargs['instance']

    if issubclass(sender, OwnershipMixin) and kwargs.get('created'):
        owner = model_obj.owner
        assign_perm('view_' + sender.__name__.lower(), owner, model_obj)
        assign_perm('change_' + sender.__name__.lower(), owner, model_obj)
        assign_perm('delete_' + sender.__name__.lower(), owner, model_obj)

    # Movement subclass
    if (issubclass(sender, Movement) and not (sender is Movement)
            and kwargs.get('created')):
        owner = model_obj.owner
        mov = Movement.objects.get(id=model_obj.movement_id)
        assign_perm('view_' + Movement.__name__.lower(), owner, mov)
        assign_perm('change_' + Movement.__name__.lower(), owner, mov)
        assign_perm('delete_' + Movement.__name__.lower(), owner, mov)


def generate_permissions():
    """
    Functions used to generate permissions strings in order to assign
    to a newly created user
    :return list result: A list with all the permissions to add
    """
    permission_list = []
    for m, p in MODEL_CLASSES_PERMS.items():
        for perm in p:
            permission_list.append(perm + '_' + m)

    permission_objs = Permission.objects.filter(
        content_type__app_label='budget').filter(codename__in=permission_list)

    return permission_objs
