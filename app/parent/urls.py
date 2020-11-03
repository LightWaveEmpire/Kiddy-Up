from django.contrib import admin
from django.urls import include, path
from . import views
from .views import *

#from django.conf import settings

urlpatterns = [
    path('', views.DashboardView.as_view(), name="home"),
    # path("parent/dashboard/", views.parent, name="dashboard"),
    path('parent/dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path("parent/profile/", views.profile, name="profile"),
    path("parent/child_login/", views.child_login, name="child_login"),


    path("register/", views.ParentSignUpView.as_view(), name="register"),
    path("parent/child_register/", views.ChildSignUpView.as_view(), name="child_register"),


    path('parent/settings/', views.SettingsView.as_view(), name='settings'),


    path('parent/rewards/', views.RewardListView.as_view(), name='rewards'),
    path('parent/reward/<int:pk>/', views.RewardDetailView.as_view(), name='reward'),
    path('parent/reward/add/', RewardCreate.as_view(), name='reward-add'),
    path('parent/reward/<int:pk>/update/', RewardUpdate.as_view(), name='reward-update'),
    path('parent/reward/<int:pk>/delete/', RewardDelete.as_view(), name='reward-delete'),


    path('parent/tasks/', views.TaskListView.as_view(), name='tasks'),
    path('parent/task/<int:pk>/', views.TaskDetailView.as_view(), name='task'),
    path('parent/task/add/', TaskCreate.as_view(), name='task-add'),
    path('parent/task/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('parent/task/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),


    path('parent/original_tasks/', views.Original_TaskListView.as_view(), name='original_tasks'),
    path('parent/original_task/<int:pk>/', views.Original_TaskDetailView.as_view(), name='original_task'),
    path('parent/original_task/add/', Original_TaskCreate.as_view(), name='original_task-add'),
    path('parent/original_task/<int:pk>/update/', Original_TaskUpdate.as_view(), name='original_task-update'),
    path('parent/original_task/<int:pk>/delete/', Original_TaskDelete.as_view(), name='original_task-delete'),


    path('parent/children/', views.ChildListView.as_view(), name='children'),
    path('parent/child/<int:pk>/', views.ChildDetailView.as_view(), name='child'),
#     path('child/add/', ChildCreate.as_view(), name='child-add'),
    path('parent/child/<int:pk>/update/', ChildUpdate.as_view(), name='child-update'),
    path('parent/child/<int:pk>/delete/', ChildDelete.as_view(), name='child-delete'),

    path('parents/', views.ParentListView.as_view(), name='parents'),
    path('parent/<int:pk>/', views.ParentDetailView.as_view(), name='parent'),
#    path('parent/add/', ParentCreate.as_view(), name='parent-add'),
    path('parent/<int:pk>/update/', ParentUpdate.as_view(), name='parent-update'),
    path('parent/<int:pk>/delete/', ParentDelete.as_view(), name='parent-delete'),

#    path('link-source/', LinkSource.as_view(), name='link-source'),


# Child Views
    path('child/profile/', views.ChildProfileView.as_view(), name='child-profile'),
    path('child/update/profile/', views.ChildUpdateProfileView.as_view(), name='child-profile-update'),
    path('child/tasks/', views.ChildTaskListView.as_view(), name='child-tasks'),
    path('child/task/<int:pk>/', views.ChildTaskDetailView.as_view(), name='child-task'),
    path('child/rewards/', views.ChildRewardListView.as_view(), name='child-rewards'),
    path('child/dashboard/', views.ChildDashboardView.as_view(), name="child-dashboard"),

]
