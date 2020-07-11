"""
Module used to store the Movement serializer class, used to
serialize a movement.
"""
from budget.models.movement import Movement
from rest_framework import serializers


class MovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movement
        fields = [
            'id',
            'unique_name',
            'description',
            'amount'
        ]
