"""
Module used to store the Budget serializer class, used to
serialize a budget.
"""
from budget.models.budget import Budget
from rest_framework import serializers
from dotp_users.serializers.mixins import OwnerModelSerializerMixin
from budget.serializers.movement_serializer import MovementSerializer


class BudgetSerializer(OwnerModelSerializerMixin):

    available_amount = serializers.FloatField(default=0.0, required=False)
    movement_objects = MovementSerializer(
        read_only=True,
        many=True,
        source='movements'
    )

    class Meta:
        model = Budget
        fields = [
            'id',
            'unique_name',
            'description',
            'available_amount',
            'movement_objects',
        ]
        examples = {
            "id": 1,
            "unique_name": "feeding_budget",
            "description": "Feeding budget",
            "available_amount": 324.55,
        }
