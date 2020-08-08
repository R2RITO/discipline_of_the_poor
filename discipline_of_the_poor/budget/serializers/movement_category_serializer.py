"""
Module used to store the MovementCategory serializer class, used to
serialize a movement category.
"""
from budget.models.movement_category import MovementCategory
from rest_framework import serializers


class MovementCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementCategory
        fields = [
            'id',
            'unique_name',
            'description',
        ]
