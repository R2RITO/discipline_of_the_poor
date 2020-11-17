"""
Module used to store the SingleMovement view class, used to
manage the movement resource
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from budget.models.single_movement import SingleMovement
from budget.models.budget_movement import BudgetMovement
from budget.models.budget import Budget
from budget.serializers.single_movement_serializer import (
    SingleMovementSerializer)
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


class SingleMovementViewSet(viewsets.ModelViewSet):

    queryset = SingleMovement.objects.all()
    serializer_class = SingleMovementSerializer

    def create(self, request, *args, **kwargs):
        # Validate the budget and the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        budget = Budget.objects.get(pk=request.data.get('budget'))

        if not user.has_perm('budget.view_budget', budget):
            error = {
                'budget': [_('Invalid budget ownership')]
            }
            raise ValidationError(error)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Validate the budget and the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if request.data.get('budget'):
            budget = Budget.objects.get(pk=request.data.get('budget'))

            if not user.has_perm('budget.view_budget', budget):
                error = {
                    'budget': [_('Invalid budget ownership')]
                }
                raise ValidationError(error)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        b_mv = BudgetMovement.objects.filter(
            movement=instance.movement).first()
        b_mv.delete()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
