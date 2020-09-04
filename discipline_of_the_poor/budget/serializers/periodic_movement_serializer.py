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


class PeriodicMovementSerializer(OwnerModelSerializerMixin):

    movement = MovementSerializer(required=True)
    budget_object = BudgetSerializer(read_only=True, source='budget')
    budget = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Budget.objects.all(),
        required=True,
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

    def create(self, validated_data):
        movement_data = validated_data.pop('movement', {})
        data = {**validated_data, **movement_data}
        periodic_movement = PeriodicMovement.objects.create(
            **data
        )
        return periodic_movement
