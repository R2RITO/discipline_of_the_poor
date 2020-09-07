"""
Budget app URLs
"""
from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from budget.views.budget_view import BudgetViewSet
from budget.views.movement_view import MovementViewSet
from budget.views.movement_category_view import MovementCategoryViewSet
from budget.views.single_movement_view import SingleMovementViewSet
from budget.views.periodic_movement_view import PeriodicMovementViewSet
from budget.views.budget_share_view import BudgetShareViewSet


router = routers.DefaultRouter()
router.register(r'budget/share', BudgetShareViewSet)
router.register(r'budget', BudgetViewSet)
router.register(r'movement', MovementViewSet)
router.register(r'single_movement', SingleMovementViewSet)
router.register(r'periodic_movement', PeriodicMovementViewSet)
router.register(r'movement_category', MovementCategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
