"""
Module used to store the BudgetShare view class, used to
manage the budget sharing
"""
from rest_framework import viewsets
from rest_framework import mixins
from budget.models.budget import Budget
from budget.serializers.budget_share_serializer import (
    BudgetShareSerializer)
from discipline_of_the_poor.permissions import OwnershipPermission


class BudgetShareViewSet(mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetShareSerializer

    permission_classes = [OwnershipPermission]
