"""
Module used to store the Budget serializer class, used to
serialize a budget.
"""
from budget.models.budget import Budget
from rest_framework import serializers


class BudgetSerializer(serializers.ModelSerializer):

    available_amount = serializers.FloatField(default=0.0, required=False)

    class Meta:
        model = Budget
        fields = [
            'id',
            'unique_name',
            'description',
            'available_amount'
        ]
