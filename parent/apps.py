from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ParentConfig(AppConfig):
    name = 'parent'

    def ready(self):
        import parent.signals.handlers
        from parent.signals.signals import populate_models
        post_migrate.connect(populate_models, sender=self)

