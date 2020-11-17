"""
Module used to store the SingleMovement serializer class, used to
serialize a movement.
"""
from budget.models.single_movement import SingleMovement
from budget.models.budget import Budget
from budget.models.budget_movement import BudgetMovement
from budget.serializers.movement_serializer import MovementSerializer
from rest_framework import serializers
from dotp_users.serializers.mixins import OwnerModelSerializerMixin


class SingleMovementSerializer(OwnerModelSerializerMixin):

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
        examples = {
            "budget": 1,
        }

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PATCH":
            fields['movement'].required = False
            fields['budget'].required = False
        return fields

    def create(self, validated_data):
        movement_data = validated_data.pop('movement', {})
        budget = validated_data.pop('budget', None)

        single_movement = super(SingleMovementSerializer, self).create(
            movement_data
        )
        category = single_movement.movement.category.unique_name
        direction = True if category == 'income' else False

        budget_movement_data = {
            'budget': budget,
            'movement': single_movement.movement,
            'direction': direction,
            'owner': single_movement.owner,
        }

        charge = BudgetMovement.objects.create(**budget_movement_data)

        return single_movement

    def update(self, instance, validated_data):
        movement_data = validated_data.pop('movement', {})
        budget = validated_data.pop('budget', None)

        b_mv = BudgetMovement.objects.filter(
            movement=instance.movement).first()

        if (budget is not None or
                movement_data.get('amount', None) is not None or
                movement_data.get('category', None) is not None):
            # Delete old BudgetMovement
            b_mv.delete()
            budget.refresh_from_db()

            # Update the movement instance to create new BudgetMovement
            for k, v in movement_data.items():
                setattr(instance, k, v)

            instance.save()

            # Create new BudgetMovement
            category = instance.movement.category.unique_name
            direction = True if category == 'income' else False

            budget_movement_data = {
                'budget': budget,
                'movement': instance.movement,
                'direction': direction,
                'owner': instance.owner,
            }

            charge = BudgetMovement.objects.create(**budget_movement_data)

        else:
            for k, v in movement_data.items():
                setattr(instance, k, v)

            instance.save()

        return instance
