from django.apps import AppConfig
import vinaigrette


class BudgetConfig(AppConfig):
    name = 'budget'

    def ready(self):
        from budget.signals import permission_signals
        MovementCategory = self.get_model('MovementCategory')

        # Register fields to translate
        vinaigrette.register(MovementCategory, ['description'])
