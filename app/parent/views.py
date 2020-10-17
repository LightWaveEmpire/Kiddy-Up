# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .forms import ParentCreationForm
from django.urls import reverse
from parent.permissions import is_in_group_parent
from parent.models import Child, Task, Reward
from django.views import generic


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
def edit_task(request):
    return render(request, "parent/edit_task.html")

@login_required
@user_passes_test(is_in_group_parent)
def edit_reward(request):
    return render(request, "parent/edit_reward.html")

@login_required
@user_passes_test(is_in_group_parent)
def edit_child(request):
    return render(request, "parent/edit_child.html")


@login_required
@user_passes_test(is_in_group_parent)
def child_login(request):
    return render(request, "parent/child_login.html")


## Switching all views over to class view (much simpler to use)
## I still need to ensure they require auth to access
## Also need to identify how to link rewards, tasks, children to parent/logged in user

class RewardListView(generic.ListView):
    model=Reward
    paginate_by = 10


class RewardDetailView(generic.DetailView):
    model = Reward

class TaskListView(generic.ListView):
    model=Task
    paginate_by = 10


class TaskDetailView(generic.DetailView):
    model = Task

class ChildListView(generic.ListView):
    model=Child
    paginate_by = 10


class ChildDetailView(generic.DetailView):
    model = Child



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
