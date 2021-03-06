from django.contrib import admin
from django.urls import include, path
from . import views
from .views import *
from django.conf.urls import include, url

#from django.conf import settings

urlpatterns = [


    path('parent/redirect/', views.redirect_on_login, name='login-redirect'),
    path('parent/pull_tasks', views.pull_tasks, name="pull_tasks"),
    path('google_oauth/redirect/', RedirectOauthView, name='google_oauth'),
    path('google_oauth/callback/', CallbackView, name='google_callback'),



    path('parent/dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path("parent/profile/", views.profile, name="profile"),
    path("parent/child_login/pre", views.pre_child_login, name="pre_child_login"),
    path("parent/child_login/", views.ChildLoginView.as_view(), name="child_login"),
    path('parent/set_active/<int:pk>/', SetActiveChildView, name='set_active_child'),

    path ("register/", views.ParentSignUpView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    # path("parent/child_register/", views.ChildSignUpView.as_view(), name="child_register"),


    path('parent/settings/', views.SettingsView.as_view(), name='settings'),


    path('parent/rewards/', views.RewardListView.as_view(), name='rewards'),
    path('parent/reward/<int:pk>/', views.RewardDetailView.as_view(), name='reward'),
    path('parent/reward/add/', RewardCreate.as_view(), name='reward-add'),
    path('parent/reward/<int:pk>/update/', RewardUpdate.as_view(), name='reward-update'),
    path('parent/reward/<int:pk>/delete/', RewardDelete.as_view(), name='reward-delete'),

    path('parent/locations/', views.LocationListView.as_view(), name='locations'),
    path('parent/location/<int:pk>/', views.LocationDetailView.as_view(), name='location'),
    path('parent/location/add/', LocationCreate.as_view(), name='location-add'),
    path('parent/location/<int:pk>/update/', LocationUpdate.as_view(), name='location-update'),
    path('parent/location/<int:pk>/delete/', LocationDelete.as_view(), name='location-delete'),

    path('parent/earned_rewards/', views.EarnedRewardListView.as_view(), name='earned_rewards'),
    path('parent/earned_reward/<int:pk>/', views.EarnedRewardDetailView.as_view(), name='earned_reward'),
    path('parent/earned_reward/<int:pk>/delete/', EarnedRewardDelete.as_view(), name='earned_reward-delete'),

    path('parent/tasks/pending', views.PendingTaskListView.as_view(), name='pending_tasks'),
    path('parent/tasks/complete', views.CompletedTaskListView.as_view(), name='completed_tasks'),
    path('parent/tasks/', views.TaskListView.as_view(), name='tasks'),
    path('parent/task/<int:pk>/', views.TaskDetailView.as_view(), name='task'),
    path('parent/task/add/', TaskCreate.as_view(), name='task-add'),
    path('parent/task/<int:pk>/update/', TaskUpdate.as_view(), name='task-update'),
    path('parent/task/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),

    path('parent/task/<int:pk>/validate/', TaskValidate, name='task-validate'),
    path('parent/task/<int:pk>/invalidate/', TaskInvalidate, name='task-invalidate'),

    path('parent/manual_add/', Original_TaskCreate.as_view(), name='manual_add'),

    path('parent/original_tasks/', views.Original_TaskListView.as_view(), name='original_tasks'),
    path('parent/original_task/<int:pk>/', views.Original_TaskDetailView.as_view(), name='original_task'),
    path('parent/original_task/add/', Original_TaskCreate.as_view(), name='original_task-add'),
    path('parent/original_task/<int:pk>/update/', Original_TaskUpdate.as_view(), name='original_task-update'),
    path('parent/original_task/<int:pk>/delete/', Original_TaskDelete.as_view(), name='original_task-delete'),


    path('parent/children/', views.ChildListView.as_view(), name='children'),
    path('parent/child/<int:pk>/', views.ChildDetailView.as_view(), name='child'),
    path('parent/child/add/', ChildCreate.as_view(), name='child-add'),
    path('parent/child/<int:pk>/update/', ChildUpdate.as_view(), name='child-update'),
    path('parent/child/<int:pk>/delete/', ChildDelete.as_view(), name='child-delete'),

    path('parents/', views.ParentListView.as_view(), name='parents'),
    path('parent/<int:pk>/', views.ParentDetailView.as_view(), name='parent'),
    #    path('parent/add/', ParentCreate.as_view(), name='parent-add'),
    # path('parent/<int:pk>/update/', ParentUpdate.as_view(), name='parent-update'),
    path('parent/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('parent/<int:pk>/delete/', ParentDelete.as_view(), name='parent-delete'),

    #    path('link-source/', LinkSource.as_view(), name='link-source'),


# Child Views
    path('child/profile/', views.ChildProfileView.as_view(), name='child-profile'),
    path('child/update/profile/<int:pk>/', views.ChildUpdateProfileView.as_view(), name='child-profile-update'),
    path('child/tasks/', views.ChildTaskListView.as_view(), name='child-tasks'),
    path('child/task/<int:pk>/', views.ChildTaskDetailView.as_view(), name='child-task'),
    path('child/task/<int:pk>/complete/', TaskCompleteView, name='task-complete'),
    path('child/rewards/', views.ChildRewardListView.as_view(), name='child-rewards'),
    path('child/reward/<int:pk>/', views.ChildRewardDetailView.as_view(), name='child-reward'),
    path('child/reward/<int:pk>/buy/', views.ChildRewardBuyView, name='reward-buy'),
    path('child/dashboard/', views.ChildDashboardView.as_view(), name="child-dashboard"),
    path('child/earned_rewards/', views.ChildEarnedRewardListView.as_view(), name='child_earned_rewards'),

]
