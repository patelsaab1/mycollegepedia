from django.apps import AppConfig


class CollegeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'College'
    verbose_name = 'COLLEGE SETTINGS'

    # def ready(self):
    #         import College.signals