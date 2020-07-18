"""
Module used to store the PeriodicMovement view class, used to
manage the movement resource
"""
from rest_framework import viewsets
from budget.models.periodic_movement import PeriodicMovement
from budget.serializers.periodic_movement_serializer import (
    PeriodicMovementSerializer)


class PeriodicMovementViewSet(viewsets.ModelViewSet):

    queryset = PeriodicMovement.objects.all()
    serializer_class = PeriodicMovementSerializer
