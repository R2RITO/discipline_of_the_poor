"""
Module used to store the MovementCategory serializer class, used to
serialize a movement category.
"""
from budget.models.movement_category import MovementCategory
from rest_framework import serializers
from django.utils.translation import gettext as _


class MovementCategorySerializer(serializers.ModelSerializer):

    description = serializers.SerializerMethodField()

    class Meta:
        model = MovementCategory
        fields = [
            'id',
            'unique_name',
            'description',
        ]

    @staticmethod
    def get_description(self):
        """
        Get translated description
        :return:
        """
        # Translators: Translation for movement category description
        return _(self.description)
