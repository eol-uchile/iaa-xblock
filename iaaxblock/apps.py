from django.apps import AppConfig
from edx_django_utils.plugins.constants import (
    ProjectType, SettingsType, PluginURLs, PluginSettings, PluginContexts
)


class IAAAppConfig(AppConfig):
    name = 'iaaxblock'
    verbose_name = "Iterative Assessed Activity XBlock"

    plugin_app = {
        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: '',
            },
            ProjectType.CMS: {
                PluginURLs.NAMESPACE: '',
            }
        },
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
            ProjectType.CMS: {
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            }
        },
    }

    def ready(self):
        pass
