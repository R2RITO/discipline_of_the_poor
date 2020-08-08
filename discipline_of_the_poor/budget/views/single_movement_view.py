"""
Module used to store the SingleMovement view class, used to
manage the movement resource
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from budget.models.single_movement import SingleMovement
from budget.models.budget_movement import BudgetMovement
from budget.serializers.single_movement_serializer import (
    SingleMovementSerializer)


class SingleMovementViewSet(viewsets.ModelViewSet):

    queryset = SingleMovement.objects.all()
    serializer_class = SingleMovementSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        b_mv = BudgetMovement.objects.filter(
            movement=instance.movement).first()
        b_mv.delete()

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
