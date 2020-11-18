# views.py
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
# from django.contrib.auth.models import User
#from .forms import ParentCreationForm
from django.urls import reverse, reverse_lazy
from .permissions import is_in_group_parent
#from .models import Child, Task, Reward, Parent, Original_Task
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from parent.forms import ParentSignUpForm, ChildSignUpForm, ChildUpdateForm, TaskUpdateForm, ChildUpdateProfileForm
from parent.models import Child, Task, Reward, Parent, Original_Task, User, Earned_Reward
from parent.utils import calendar_pull, task_factory, reward_system

import google_apis_oauth
import os
import os.path
import sys

'''
Views to authenticate with Google and pull events and tasks
'''

# The url where the google oauth should redirect
# after a successful login.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
REDIRECT_URI = 'http://localhost:8080/google_oauth/callback/'

# Authorization scopes required
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/tasks.readonly']

# Path of the "client_id.json" file
current_path = os.path.dirname(__file__)
JSON_FILEPATH = os.path.join(current_path, 'client_id.json')

@login_required
@user_passes_test(is_in_group_parent)
def RedirectOauthView(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)

@login_required
@user_passes_test(is_in_group_parent)
def CallbackView(request):
    try:
        # Get user credentials
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request,
            JSON_FILEPATH,
            SCOPES,
            REDIRECT_URI
        )

        # Stringify credentials for storing them in the DB
        stringified_token = google_apis_oauth.stringify_credentials(
            credentials)

        # Store the credentials safely in the DB
        parent = Parent.objects.get(user = request.user)
        parent.account_creds = stringified_token
        parent.save()

        # Now that you have stored the user credentials you
        # can redirect user to your main application.
        return redirect('settings')
    except:
        print(f'Error occurred when getting oauth credentials')
        raise
        return redirect('settings')



@login_required
@user_passes_test(is_in_group_parent)
def pull_tasks(request):
    try:
        service = calendar_pull.login_calendar(request.user)
        list_of_events = calendar_pull.get_list_of_events(service, 100)
        for event, json_event in list_of_events:
            print(f'\n\nDEBUG: {event}\n\n{json_event}\n\n', file=sys.stderr)
    except:
        print("Unexpected error in Calendar Pull:")
        raise
    parent = Parent.objects.get(user = request.user)
    task_factory.create_otasks_from_list(parent, list_of_events)
    return redirect('dashboard')






# Require Login

# @login_required
# @user_passes_test(is_in_group_parent)
# def parent(request):
#     return render(request, "parent/dashboard.html")

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'parent/dashboard.html'

    def children(self):
        return Child.objects.filter(parent__user = self.request.user)

    def rewards(self):
        return Reward.objects.filter(parent__user = self.request.user)

    def tasks(self):
        return Task.objects.filter(parent__user = self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True


@login_required
@user_passes_test(is_in_group_parent)
def profile(request):
    return render(request, "parent/profile.html")


@login_required
@user_passes_test(is_in_group_parent)
def child_login(request):
    return render(request, "parent/child_login.html")


@login_required
def redirect_on_login(request):
    if request.user.is_parent ==  True:
        return redirect('dashboard')
    else:
        return redirect('child-dashboard')



# Reward Views

class RewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Reward
    paginate_by = 10

    def get_queryset(self):
        return Reward.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True



class RewardDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Reward

    def test_func(self):
        return self.request.user.is_parent == True

class RewardCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Reward
    fields = ['name', 'cost']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_parent == True

class RewardUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Reward
    fields = ['name', 'cost']

    def test_func(self):
        return self.request.user.is_parent == True

class RewardDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Reward
    success_url = reverse_lazy('rewards')

    def test_func(self):
        return self.request.user.is_parent == True



# Earned Reward Views



class EarnedRewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Earned_Reward
    paginate_by = 10

    def get_queryset(self):
        return Earned_Reward.objects.filter(child__parent__user=self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True



class EarnedRewardDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Earned_Reward

    def test_func(self):
        return self.request.user.is_parent == True


class EarnedRewardDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Earned_Reward
    success_url = reverse_lazy('earned-rewards')

    def test_func(self):
        return self.request.user.is_parent == True









# Original_Task Views

class Original_TaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Original_Task
    paginate_by = 10

    def get_queryset(self):
        return Original_Task.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True



class Original_TaskDetailView(generic.DetailView):
    model = Original_Task

    def test_func(self):
        return self.request.user.is_parent == True


class Original_TaskCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Original_Task
    fields = ['otask']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
#        form.instance.parent = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_parent == True


class Original_TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Original_Task
    fields = ['otask']

    def test_func(self):
        return self.request.user.is_parent == True


class Original_TaskDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Original_Task
    success_url = reverse_lazy('original_tasks')

    def test_func(self):
        return self.request.user.is_parent == True









## Task Views

class CompletedTaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Task
    paginate_by = 10
    template_name = "parent/completed_task_list.html"

    def get_queryset(self):
        return Task.objects.filter(parent__user=self.request.user, status='COMP')

    def test_func(self):
        return self.request.user.is_parent == True


class TaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Task
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True



class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task

    def test_func(self):
        return self.request.user.is_parent == True


class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Task
    fields = ['name', 'description', 'point_value', 'child', 'date']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
#        form.instance.parent = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_parent == True



class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "parent/task_form.html"

    def test_func(self):
        return self.request.user.is_parent == True

class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return self.request.user.is_parent == True







# Child Views

class ChildListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Child
    paginate_by = 10

    def get_queryset(self):
        return Child.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True



class ChildDetailView(generic.DetailView):
    model = Child

    def test_func(self):
        return self.request.user.is_parent == True





class ChildCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Child
    fields = ['age', 'comp_level', 'target_reward']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
#        form.instance.parent = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_parent == True




class ChildUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Child
    form_class = ChildUpdateForm
    template_name = "parent/child_form.html"

    def test_func(self):
        return self.request.user.is_parent == True




class ChildDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Child
    success_url = reverse_lazy('children')

    def test_func(self):
        return self.request.user.is_parent == True




# Parent Views


class ParentListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Parent
    paginate_by = 10

    def get_queryset(self):
        return Parent.objects.filter(user=self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True



class ParentDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Parent

    def test_func(self):
        return self.request.user.is_parent == True



#class ParentCreate(LoginRequiredMixin, generic.CreateView):
#    model = Parent
#    fields = ['zip_code']
#
#    def form_valid(self, form):
#        form.instance.user = self.request.user
#        return super().form_valid(form)


class ParentUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Parent
    fields = ['zip_code']

    def test_func(self):
        return self.request.user.is_parent == True


class ParentDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Parent
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_parent == True



# No Login Required




def home(request):
    return render(request, "parent/index.html")


# def register(request):
#     if request.method == "GET":
#        return render(
#         request, "parent/register.html",
#            {"form": ParentCreationForm}
#        )
#    elif request.method == "POST":
#        form = ParentCreationForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            login(request, user)
#            return redirect("home")
#

class ParentSignUpView(generic.CreateView):
    model = User
    form_class = ParentSignUpForm
    template_name = "parent/register.html"

    def get_context_date(self, **kwargs):
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')

class ChildSignUpView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = User
    form_class = ChildSignUpForm
    template_name = "parent/child_register.html"
    def get_initial(self):
        initial = super().get_initial()
        initial['parent'] = Parent.objects.get(user=self.request.user)
        return initial

#    def get_context_date(self, **kwargs):
#        kwargs['user_type'] = 'child'
#        kwargs['parent'] = Parent.objects.get(user=self.request.user)

#        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        age = form.cleaned_data['age']
        comp_level = form.cleaned_data['comp_level']
        name = form.cleaned_data['name']
        user = form.save()
        user.is_child=True
        parent = Parent.objects.get(user=self.request.user)
        child = Child.objects.create(user=user, parent=parent, age=age, name=name, comp_level=comp_level)
        return redirect('dashboard')

    def test_func(self):
        return self.request.user.is_parent == True





# class ChildUpdateView(generic.UpdateView):
#     model = Child
#     form_class = ChildSignUpForm
#     template_name = "parent/child_register.html"

#     def form_valid(self, form):
#         age = form.cleaned_data['age']
#         user = form.save()
#         user.is_child=True
#         parent = Parent.objects.get(user=self.request.user)
#         child = Child.objects.create(user=user, parent=parent, age=age)
#         return redirect('dashboard')





# Settings

class SettingsView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'parent/settings.html'

    def parent(self):
        return Parent.objects.filter(user = self.request.user)
    def rewards(self):
        return Reward.objects.filter(parent__user = self.request.user)
    def tasks(self):
        return Task.objects.filter(parent__user = self.request.user)
    def children(self):
        return Child.objects.filter(parent__user = self.request.user)

    def test_func(self):
        return self.request.user.is_parent == True


# Child Views

class ChildDashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'parent/child_dashboard.html'

    def child(self):
        return Child.objects.filter(user = self.request.user)
    def rewards(self):
        return Reward.objects.filter(parent__user = self.request.user)
    def tasks(self):
        return Task.objects.filter(child__user = self.request.user)

    def test_func(self):
        return self.request.user.is_active == True

class ChildProfileView(generic.TemplateView):
    model = Child
    template_name = 'parent/child_profile.html'

    def child(self):
        return Child.objects.filter(user = self.request.user)

    def test_func(self):
        return self.request.user.is_active == True


class ChildUpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    model = Child
    form_class = ChildUpdateProfileForm
    template_name = "parent/child_update_profile_form.html"

    def child(self):
        return Child.objects.filter(user = self.request.user)

    def test_func(self):
        return self.request.user.is_active == True


class ChildTaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    model=Task
    template_name = 'parent/child_task_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(child__user=self.request.user)

    def test_func(self):
        return self.request.user.is_active == True

class ChildRewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    model=Reward
    template_name = 'parent/child_reward_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_active == True


class ChildTaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task
    template_name = 'parent/child_task.html'

    def test_func(self):
        return self.request.user.is_active == True
