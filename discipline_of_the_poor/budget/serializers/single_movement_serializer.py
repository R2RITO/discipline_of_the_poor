"""
Module used to store the SingleMovement serializer class, used to
serialize a movement.
"""
from budget.models.single_movement import SingleMovement
from budget.serializers.movement_serializer import MovementSerializer
from rest_framework import serializers


class SingleMovementSerializer(serializers.ModelSerializer):

    movement = MovementSerializer(required=True)

    class Meta:
        model = SingleMovement
        fields = [
            'movement',
        ]

    def create(self, validated_data):
        movement_data = validated_data.pop('movement', {})
        single_movement = SingleMovement.objects.create(
            **movement_data
        )
        return single_movement
