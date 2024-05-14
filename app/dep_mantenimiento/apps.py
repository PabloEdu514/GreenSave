from django.apps import AppConfig


class depConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dep_mantenimiento'
    def ready(self):
        import dep_mantenimiento.signals  # Importar el archivo signals.py
        