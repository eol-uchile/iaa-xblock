from django.apps import AppConfig


class IAAAppConfig(AppConfig):
    name = "iaaxblock"
    verbose_name = "Iterative Assessed Activity XBlock"

    def ready(self):
        pass
