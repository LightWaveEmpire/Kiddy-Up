from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(Task)
admin.site.register(Reward)
