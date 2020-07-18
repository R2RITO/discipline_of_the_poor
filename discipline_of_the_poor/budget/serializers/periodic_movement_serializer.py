"""
Module used to store the PeriodicMovement serializer class, used to
serialize a movement.
"""
from budget.models.periodic_movement import PeriodicMovement
from budget.serializers.movement_serializer import MovementSerializer
from rest_framework import serializers


class PeriodicMovementSerializer(serializers.ModelSerializer):

    movement = MovementSerializer(required=True)

    class Meta:
        model = PeriodicMovement
        fields = [
            'type',
            'day_of_week',
            'day_of_month',
            'time',
            'movement',
        ]

    def create(self, validated_data):
        movement_data = validated_data.pop('movement', {})
        data = {**validated_data, **movement_data}
        periodic_movement = PeriodicMovement.objects.create(
            **data
        )
        return periodic_movement
