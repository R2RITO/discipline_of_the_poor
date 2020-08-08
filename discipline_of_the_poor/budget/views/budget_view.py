"""
Module used to store the Budget view class, used to
manage the budget resource
"""
from rest_framework import viewsets
from budget.models.budget import Budget
from budget.serializers.budget_serializer import BudgetSerializer


class BudgetViewSet(viewsets.ModelViewSet):

    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
