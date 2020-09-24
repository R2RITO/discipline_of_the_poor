"""
Module used to store the Budget serializer class, used to
serialize a budget.
"""
from budget.models.budget import Budget
from rest_framework import serializers
from dotp_users.serializers.mixins import OwnerModelSerializerMixin
from budget.serializers.movement_serializer import MovementSerializer
from budget.business.budget_stats.base import get_budget_stats
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


class BudgetSerializer(OwnerModelSerializerMixin):

    available_amount = serializers.FloatField(default=0.0, required=False)
    movement_objects = MovementSerializer(
        read_only=True,
        many=True,
        source='movements'
    )
    stats = serializers.SerializerMethodField(required=False)

    def get_stats(self, obj):
        user = obj.owner
        return get_budget_stats(user, obj)

    class Meta:
        model = Budget
        fields = [
            'id',
            'unique_name',
            'description',
            'available_amount',
            'movement_objects',
            'stats',
        ]
        examples = {
            "id": 1,
            "unique_name": "feeding_budget",
            "description": "Feeding budget",
            "available_amount": 324.55,
            "stats": {
                "message": "congrats premium user!"
            }
        }
        write_once_fields = ('available_amount',)

    def update(self, instance, validated_data):

        # Validate non-update fields
        for field in self.Meta.write_once_fields:
            if field in validated_data:
                raise ValidationError(
                    _("The field {field} cannot be updated".format(field=field))
                )

        return super().update(instance, validated_data)
