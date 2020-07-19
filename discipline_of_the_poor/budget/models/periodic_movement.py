"""
Module for the PeriodicMovement model, used to handle movements that are
executed every set amount of time
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from budget.models.movement import Movement
from budget.models.budget import Budget


class PeriodicMovement(Movement):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    TYPE_CHOICES = [
        (DAILY, _('Daily period')),
        (WEEKLY, _('Weekly period')),
        (MONTHLY, _('Monthly period')),
    ]
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=MONTHLY,
    )
    day_of_week = models.CharField(max_length=50, null=True)
    day_of_month = models.CharField(max_length=10, null=True)
    time = models.TimeField(default=timezone.now().time)
    movement = models.OneToOneField(
        Movement,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )
    budget = models.ForeignKey(Budget, on_delete=models.DO_NOTHING)
