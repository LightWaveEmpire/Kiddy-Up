# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from .forms import ParentCreationForm
from django.urls import reverse, reverse_lazy
from parent.permissions import is_in_group_parent
from parent.models import Child, Task, Reward, Parent
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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
def child_login(request):
    return render(request, "parent/child_login.html")


## Switching all views over to class view (much simpler to use)
## I still need to ensure they require auth to access
## Also need to identify how to link rewards, tasks, children to parent/logged in user



# Reward Views

class RewardListView(generic.ListView):
    model=Reward
    paginate_by = 10

    def get_queryset(self):
        return Reward.objects.filter(created_by_id=self.request.user)


class RewardDetailView(generic.DetailView):
    model = Reward

class RewardCreate(LoginRequiredMixin, generic.CreateView):
    model = Reward
    fields = ['rname', 'cost']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class RewardUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Reward
    fields = ['rname', 'cost']

class RewardDelete(LoginRequiredMixin, generic.DeleteView):
    model = Reward
    success_url = reverse_lazy('rewards')








# Task Views

class TaskListView(generic.ListView):
    model=Task
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(created_by_id=self.request.user)


class TaskDetailView(generic.DetailView):
    model = Task

class TaskCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = ['tname', 'tdesc', 'point_value', 'owner', 'date']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = ['tname', 'tdesc', 'point_value', 'owner', 'date']

class TaskDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')






# Child Views

class ChildListView(generic.ListView):
    model=Child
    paginate_by = 10

    def get_queryset(self):
        return Child.objects.filter(created_by_id=self.request.user)


class ChildDetailView(generic.DetailView):
    model = Child



class ChildCreate(LoginRequiredMixin, generic.CreateView):
    model = Child
    fields = ['cname', 'age', 'comp_level', 'parent', 'target_reward']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ChildUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Child
    fields = ['cname', 'age', 'comp_level', 'parent', 'target_reward']

class ChildDelete(LoginRequiredMixin, generic.DeleteView):
    model = Child
    success_url = reverse_lazy('children')



# Parent Views


class ParentListView(generic.ListView):
    model=Parent
    paginate_by = 10

    def get_queryset(self):
        return Parent.objects.filter(created_by_id=self.request.user)


class ParentDetailView(generic.DetailView):
    model = Parent


class ParentCreate(LoginRequiredMixin, generic.CreateView):
    model = Parent
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ParentUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Parent
    fields = ['name']

class ParentDelete(LoginRequiredMixin, generic.DeleteView):
    model = Parent
    success_url = reverse_lazy('parents')


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
