"""
Module used to store the SingleMovement serializer class, used to
serialize a movement.
"""
from budget.models.single_movement import SingleMovement
from budget.models.budget import Budget
from budget.models.budget_movement import BudgetMovement
from budget.serializers.movement_serializer import MovementSerializer
from rest_framework import serializers


class SingleMovementSerializer(serializers.ModelSerializer):

    movement = MovementSerializer(required=True)
    budget = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Budget.objects.all(),
        required=True,
    )

    class Meta:
        model = SingleMovement
        fields = [
            'movement',
            'budget',
        ]

    def create(self, validated_data):
        movement_data = validated_data.pop('movement', {})
        budget = validated_data.pop('budget', None)

        single_movement = SingleMovement.objects.create(
            **movement_data
        )
        category = single_movement.movement.category.unique_name
        direction = True if category == 'income' else False

        movement_data = {
            'budget': budget,
            'movement': single_movement.movement,
            'direction': direction,
        }

        charge = BudgetMovement.objects.create(**movement_data)

        return single_movement
