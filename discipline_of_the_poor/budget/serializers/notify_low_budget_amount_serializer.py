"""
Module used to store the NotifyLowBudgetAmountSerializer class, used to
serialize input to update the option on the user profile
"""
from rest_framework import serializers


class NotifyLowBudgetAmountSerializer(serializers.Serializer):
    notify = serializers.BooleanField(required=True)

    class Meta:
        fields = [
            'notify',
        ]
        examples = {
            "notify": True,
        }
