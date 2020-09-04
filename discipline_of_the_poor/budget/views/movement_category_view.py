"""
Module used to store the MovementCategory view class, used to
manage the movement category resource
"""
from rest_framework import viewsets
from rest_framework import mixins
from budget.models.movement_category import MovementCategory
from budget.serializers.movement_category_serializer import (
    MovementCategorySerializer)


class MovementCategoryViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    queryset = MovementCategory.objects.all()
    serializer_class = MovementCategorySerializer
    permission_classes = []
    filter_backends = []
