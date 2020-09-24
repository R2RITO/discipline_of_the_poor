"""
Module for the Budget model, used to store all the budgets of a user with their
available amounts
"""
from django.db import models
from budget.models.mixins import BaseMixin
from budget.models.movement import Movement
from dotp_users.models.mixins import OwnershipMixin
import reversion
from django.conf import settings
import os


def get_storage_path(instance, filename):
    """
    Function used to fetch the absolute path to store the image.
    The path is created by appending the base media path and the
    user unique id as the path, and the date plus the given
    @filename as the file name
    :param Budget instance: the instance of the obj to
                                     store
    :param filename: the given file name
    :return str path: the path of the file to save
    """
    user_id = str(instance.owner_id)
    file_name = str(instance.create_date.date()) + '_' + filename
    file_path = os.path.join(
        settings.BUDGET_MEDIA_FOLDER, user_id, file_name)
    return file_path


@reversion.register()
class Budget(BaseMixin, OwnershipMixin):
    unique_name = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    available_amount = models.FloatField()
    movements = models.ManyToManyField(
        Movement,
        through='BudgetMovement',
        related_name='budgets',
    )
    photo = models.ImageField(
        upload_to=get_storage_path,
        null=True,
    )
