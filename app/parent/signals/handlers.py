from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, created, **kwargs):
    if created:
        g1 = Group.objects.get(name='parent')
        instance.groups.add(g1)

#def populate_models(sender, **kwargs):
#    from django.apps import apps
#    from .apps import ParentConfig
#    from django.contrib.auth.models import Group, Permission
#    from django.contrib.contenttypes.models import ContentType
#
#    group_app, created = Group.objects.get_or_create(name=ParentConfig.name)
#
#    models = apps.all_models[ParentConfig.name]
#    for model in models:
#        content_type = ContentType.objects.get(
#            app_label=ParentConfig.name,
#            model=model
#        )
#        permissions = Permission.objects.filter(content_type=content_type)
#        group_app.permissions.add(*permissions)
