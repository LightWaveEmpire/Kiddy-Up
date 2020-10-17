from django.contrib import admin
from django.urls import include, path
from . import views
from parent.views import *

#from django.conf import settings

urlpatterns = [
    path('', views.parent, name="home"),
    path("dashboard/", views.parent, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("child_login/", views.child_login, name="child_login"),
    path("register/", views.register, name="register"),
    path('rewards/', views.RewardListView.as_view(), name='rewards'),
    path('reward/<int:pk>', views.RewardDetailView.as_view(), name='reward'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task'),
    path('children/', views.ChildListView.as_view(), name='children'),
    path('child/<int:pk>', views.ChildDetailView.as_view(), name='child'),
    path('reward/add/', RewardCreate.as_view(), name='reward-add'),
    path('reward/<int:pk>/', RewardUpdate.as_view(), name='reward-update'),
    path('reward/<int:pk>/delete/', RewardDelete.as_view(), name='reward-delete'),
    path('task/add/', TaskCreate.as_view(), name='task-add'),
    path('task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),
    path('child/add/', ChildCreate.as_view(), name='child-add'),
    path('child/<int:pk>/', ChildUpdate.as_view(), name='child-update'),
    path('child/<int:pk>/delete/', ChildDelete.as_view(), name='child-delete'),
]
