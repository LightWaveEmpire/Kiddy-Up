from django.apps import AppConfig


class ParentConfig(AppConfig):
    name = 'parent'

    def ready(self):
        import parent.signals.handlers

#class ParentDashboardConfig(AppConfig):
#    name = 'parent_dashboard'
#
#
#class ParentProfileConfig(AppConfig):
#    name = 'parent_profile'
#
#
#class ParentSettingsConfig(AppConfig):
#    name = 'parent_settings'
