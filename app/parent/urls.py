from django.contrib import admin
from django.urls import include, path
from . import views

#from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path("dashboard/", views.parent, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("rewards/", views.rewards, name="rewards"),
    path("tasks/", views.tasks, name="tasks"),
    path("child_login/", views.child_login, name="child_login"),
    path("register/", views.register, name="register"),
]
