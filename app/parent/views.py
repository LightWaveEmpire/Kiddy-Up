# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .forms import ParentCreationForm
from django.urls import reverse
from parent.permissions import is_in_group_parent




# Create views here.


# Require Login

@login_required
@user_passes_test(is_in_group_parent)
def parent(request):
    return render(request, "parent/dashboard.html")

@login_required
@user_passes_test(is_in_group_parent)
def profile(request):
    return render(request, "parent/profile.html")

@login_required
@user_passes_test(is_in_group_parent)
def settings(request):
    return render(request, "parent/settings.html")

@login_required
@user_passes_test(is_in_group_parent)
def tasks(request):
    return render(request, "parent/tasks.html")

@login_required
@user_passes_test(is_in_group_parent)
def rewards(request):
    return render(request, "parent/rewards.html")

@login_required
@user_passes_test(is_in_group_parent)
def task(request):
#     tasks = get_tasks(1,2)

    return render(request, "parent/task.html")

@login_required
@user_passes_test(is_in_group_parent)
def reward(request):
    return render(request, "parent/reward.html")

@login_required
@user_passes_test(is_in_group_parent)
def edit_task(request):
    return render(request, "parent/edit_task.html")

@login_required
@user_passes_test(is_in_group_parent)
def edit_reward(request):
    return render(request, "parent/edit_reward.html")

@login_required
@user_passes_test(is_in_group_parent)
def child_login(request):
    return render(request, "parent/child_login.html")


# No Login Required


def home(request):
    return render(request, "parent/index.html")


def register(request):
    if request.method == "GET":
        return render(
            request, "parent/register.html",
            {"form": ParentCreationForm}
        )
    elif request.method == "POST":
        form = ParentCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
