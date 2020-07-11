"""
Budget app URLs
"""
from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from budget.views.budget_view import BudgetViewSet
from budget.views.movement_view import MovementViewSet
from budget.views.movement_category_view import MovementCategoryViewSet


router = routers.DefaultRouter()
router.register(r'budget', BudgetViewSet)
router.register(r'movement', MovementViewSet)
router.register(r'movement_category', MovementCategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
