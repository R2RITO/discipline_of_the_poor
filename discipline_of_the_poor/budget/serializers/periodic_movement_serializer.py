"""
Module used to store the PeriodicMovement serializer class, used to
serialize a movement.
"""
from budget.models.periodic_movement import PeriodicMovement
from budget.models.budget import Budget
from budget.serializers.movement_serializer import MovementSerializer
from budget.serializers.budget_serializer import BudgetSerializer
from rest_framework import serializers
from dotp_users.serializers.mixins import OwnerModelSerializerMixin
from django.utils.translation import gettext as _


DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'
TYPE_CHOICES = [
    (DAILY, _('Daily period')),
    (WEEKLY, _('Weekly period')),
    (MONTHLY, _('Monthly period')),
]


class PeriodicMovementSerializer(OwnerModelSerializerMixin):

    movement = MovementSerializer(required=True)
    budget_object = BudgetSerializer(read_only=True, source='budget')
    budget = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Budget.objects.all(),
        required=True,
    )
    type = serializers.ChoiceField(
        choices=TYPE_CHOICES,
        default=MONTHLY,
    )

    class Meta:
        model = PeriodicMovement
        fields = [
            'type',
            'day_of_week',
            'day_of_month',
            'time',
            'movement',
            'budget',
            'budget_object',
        ]
        examples = {
            "type": 'daily',
            "day_of_week": "1",
            "day_of_month": "25",
            "time": "17:43:13.170674",
            "budget": 1,
        }

    def create(self, validated_data):
        movement_data = validated_data.pop('movement', {})
        data = {**validated_data, **movement_data}
        periodic_movement = PeriodicMovement.objects.create(
            **data
        )
        return periodic_movement
