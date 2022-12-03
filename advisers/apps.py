from django.apps import AppConfig


class AdvisersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'advisers'

    def ready(self):
        from advisers.signals import signals
        assert signals, "Signals app Advisers signals required"

