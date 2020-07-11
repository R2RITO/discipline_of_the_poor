"""
Module for the MovementCategory model, used to store all the available
categories for a movement, such as expense or income
"""
from django.db import models
from budget.models.mixins import BaseMixin


class MovementCategory(BaseMixin):
    unique_name = models.CharField(unique=True, max_length=100)
    description = models.TextField()
