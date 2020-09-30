from django.contrib import admin
from django.urls import include, path
from . import views

#from django.conf import settings

urlpatterns = [
    path("", views.home, name="home_page"),
    path("parent/", views.parent, name="parent_dashboard"),
    path("profile/", views.parent, name="parent_profile"),
    path("settings/", views.parent, name="parent_settings"),
]
