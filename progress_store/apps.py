from django.apps import AppConfig


class ProgressStoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'progress_store'
    # apps.py
    def ready(self):
        import progress_store.signals

