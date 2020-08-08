"""
Module used to store the Movement serializer class, used to
serialize a movement.
"""
from budget.models.movement import Movement
from budget.models.movement_category import MovementCategory
from budget.serializers.movement_category_serializer import (
    MovementCategorySerializer)
from rest_framework import serializers


class MovementSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=MovementCategory.objects.all(),
        required=True)
    category_object = MovementCategorySerializer(
        read_only=True,
        source='category')

    class Meta:
        model = Movement
        fields = [
            'id',
            'description',
            'amount',
            'category',
            'category_object'
        ]
