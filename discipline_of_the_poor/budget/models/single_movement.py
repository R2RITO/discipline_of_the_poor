"""
Module for the SingleMovement model, used to represent a movement issued only
one time
"""
from budget.models.movement import Movement
from django.db import models
import reversion


@reversion.register()
class SingleMovement(Movement):
    movement = models.OneToOneField(
        Movement,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )
