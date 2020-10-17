from django.contrib import admin
from django.urls import include, path
from . import views

#from django.conf import settings

urlpatterns = [
    path('', views.parent, name="home"),
    path("dashboard/", views.parent, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("edit_reward/", views.edit_reward, name="edit_reward"),
    path("edit_task/", views.edit_task, name="edit_task"),
    path("edit_child/", views.edit_task, name="edit_child"),
    path("child_login/", views.child_login, name="child_login"),
    path("register/", views.register, name="register"),
    path('rewards/', views.RewardListView.as_view(), name='rewards'),
    path('reward/<int:pk>', views.RewardDetailView.as_view(), name='reward'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task'),
    path('children/', views.ChildListView.as_view(), name='children'),
    path('child/<int:pk>', views.ChildDetailView.as_view(), name='child'),
]
