#from django.dispatch import Signal

def populate_models(sender, **kwargs):
    from django.apps import apps
    from parent.apps import ParentConfig
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    group_app, created = Group.objects.get_or_create(name=ParentConfig.name)

    models = apps.all_models[ParentConfig.name]
    for model in models:
        content_type, created = ContentType.objects.get_or_create(
            app_label=ParentConfig.name,
            model=model
        )

        permissions = Permission.objects.filter(content_type=content_type)
        group_app.permissions.add(*permissions)
