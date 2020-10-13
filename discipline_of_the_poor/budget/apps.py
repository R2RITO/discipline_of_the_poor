from django.apps import AppConfig


class BudgetConfig(AppConfig):
    name = 'budget'

    def ready(self):
        from budget.signals import permission_signals
