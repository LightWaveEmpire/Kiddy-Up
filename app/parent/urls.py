from django.contrib import admin
from django.urls import include, path
from . import views
from parent.views import *

#from django.conf import settings

urlpatterns = [
    path('', views.parent, name="home"),
    path("dashboard/", views.parent, name="dashboard"),
    path("profile/", views.profile, name="profile"),
#    path("settings/", views.settings, name="settings"),
    path("child_login/", views.child_login, name="child_login"),
    path("register/", views.register, name="register"),

    path('settings/', views.SettingsView.as_view(), name='settings'),

    path('rewards/', views.RewardListView.as_view(), name='rewards'),
    path('reward/<int:pk>', views.RewardDetailView.as_view(), name='reward'),
    path('reward/add/', RewardCreate.as_view(), name='reward-add'),
    path('reward/<int:pk>/', RewardUpdate.as_view(), name='reward-update'),
    path('reward/<int:pk>/delete/', RewardDelete.as_view(), name='reward-delete'),

    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task'),
    path('task/add/', TaskCreate.as_view(), name='task-add'),
    path('task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),

    path('children/', views.ChildListView.as_view(), name='children'),
    path('child/<int:pk>', views.ChildDetailView.as_view(), name='child'),
    path('child/add/', ChildCreate.as_view(), name='child-add'),
    path('child/<int:pk>/', ChildUpdate.as_view(), name='child-update'),
    path('child/<int:pk>/delete/', ChildDelete.as_view(), name='child-delete'),

    path('parents/', views.ParentListView.as_view(), name='parents'),
    path('parent/<int:pk>', views.ParentDetailView.as_view(), name='parent'),
    path('parent/add/', ParentCreate.as_view(), name='parent-add'),
    path('parent/<int:pk>/', ParentUpdate.as_view(), name='parent-update'),
    path('parent/<int:pk>/delete/', ParentDelete.as_view(), name='parent-delete'),
]
