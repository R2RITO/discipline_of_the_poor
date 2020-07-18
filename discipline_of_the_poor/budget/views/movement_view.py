"""
Module used to store the Movement view class, used to
manage the movement resource
"""
from rest_framework import viewsets
from rest_framework import mixins
from budget.models.movement import Movement
from budget.serializers.movement_serializer import MovementSerializer


class MovementViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
