"""
Module used to store the SingleMovement view class, used to
manage the movement resource
"""
from rest_framework import viewsets
from budget.models.single_movement import SingleMovement
from budget.serializers.single_movement_serializer import (
    SingleMovementSerializer)


class SingleMovementViewSet(viewsets.ModelViewSet):

    queryset = SingleMovement.objects.all()
    serializer_class = SingleMovementSerializer
