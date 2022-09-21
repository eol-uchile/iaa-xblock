from django.apps import AppConfig
from edx_django_utils.plugins.constants import (
    ProjectType, SettingsType, PluginURLs, PluginSettings, PluginContexts
)


class IAAAppConfig(AppConfig):
    name = 'iaaxblock'
    verbose_name = "Iterative Assessed Activity XBlock"

    plugin_app = {

        # Configuration setting for Plugin URLs for this app.
        PluginURLs.CONFIG: {

            # Configure the Plugin URLs for each project type, as needed.
            ProjectType.LMS: {

                # The namespace to provide to django's urls.include.
                PluginURLs.NAMESPACE: 'iaaxblock',

                # The application namespace to provide to django's urls.include.
                # Optional; Defaults to None.
                PluginURLs.APP_NAME: 'iaaxblock',

            },
            ProjectType.CMS: {

                # The namespace to provide to django's urls.include.
                PluginURLs.NAMESPACE: 'iaaxblock',

                # The application namespace to provide to django's urls.include.
                # Optional; Defaults to None.
                PluginURLs.APP_NAME: 'iaaxblock',

            }
        },

        # Configuration setting for Plugin Settings for this app.
        PluginSettings.CONFIG: {

            # Configure the Plugin Settings for each Project Type, as needed.
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
