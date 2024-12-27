from django.apps import AppConfig


class ScrapperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrapper'

    def ready(self):
        from . import scheduler
        scheduler.run()