from django.contrib import admin
from django.urls import include, path
from . import views

#from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path("parent/dashboard/", views.parent, name="parent_dashboard"),
    path("profile/", views.profile, name="parent_profile"),
    path("settings/", views.settings, name="parent_settings"),
    path("register/", views.register, name="register"),
]
