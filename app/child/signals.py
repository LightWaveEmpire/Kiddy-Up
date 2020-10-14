def populate_models(sender, **kwargs):
    from django.apps import apps
    from .apps import ChildConfig
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    group_app, created = Group.objects.get_or_create(name=ChildConfig.name)

    models = apps.all_models[ChildConfig.name]
    for model in models:
        content_type = ContentType.objects.get(
            app_label=ChildConfig.name,
            model=model
        )
        permissions = Permission.objects.filter(content_type=content_type)
        group_app.permissions.add(*permissions)
