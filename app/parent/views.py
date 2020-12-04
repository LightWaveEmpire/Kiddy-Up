# views.py
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
#from .forms import ParentCreationForm
from django.urls import reverse, reverse_lazy
from .permissions import is_in_group_parent
#from .models import Child, Task, Reward, Parent, Original_Task
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from parent.forms import ParentSignUpForm, ChildSignUpForm, ChildUpdateForm, TaskUpdateForm, ChildUpdateProfileForm, ChildLoginForm, UpdateProfileForm
from parent.models import Child, Task, Reward, Parent, Original_Task, Earned_Reward
from parent.utils import calendar_pull, task_factory, reward_system




import google_apis_oauth
import os
import os.path
import sys
import requests




from django.views.generic import View, UpdateView
from .forms import ParentSignUpForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode




def is_member(user):
    return user.groups.filter(name='Parent').exists()


def get_weather(request):
        parent = Parent.objects.get(user = request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the
        return day_weather



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

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather

    def children(self):
        parent = Parent.objects.get(user = self.request.user)
        children = Child.objects.filter(parent = parent)
        return children

    def rewards(self):
        return Reward.objects.filter(parent__user = self.request.user)

    def earned_rewards(self):
        parent = Parent.objects.get(user = self.request.user)
        return Earned_Reward.objects.filter(child__parent = parent)

    def tasks(self):
        return Task.objects.filter(parent__user = self.request.user, status='OPEN')

    def pending_tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        return Task.objects.filter(parent = parent, status='PEND')
    
    def completed_tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        return Task.objects.filter(parent = parent, status='COMP')

    def test_func(self):
        return is_member(self.request.user)



@login_required
@user_passes_test(is_in_group_parent)
def profile(request):
    return render(request, "parent/profile.html")



@login_required
def redirect_on_login(request):
    parent = Parent.objects.get(user=request.user)
    if is_member(request.user):
        if parent.active_child:
            return redirect('child-dashboard')
        else:
            return redirect('dashboard')
    else:
        return redirect('about')



# Reward Views

class RewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Reward
    paginate_by = 10

    def get_queryset(self):
        return Reward.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class RewardDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Reward

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class RewardCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Reward
    fields = ['name', 'cost']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class RewardUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Reward
    fields = ['name', 'cost']

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class RewardDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Reward
    success_url = reverse_lazy('rewards')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


# Earned Reward Views



class EarnedRewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Earned_Reward
    paginate_by = 10

    def get_queryset(self):
        return Earned_Reward.objects.filter(child__parent__user=self.request.user)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class EarnedRewardDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Earned_Reward

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class EarnedRewardDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Earned_Reward
    success_url = reverse_lazy('earned_rewards')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



# Original_Task Views

class Original_TaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Original_Task
    paginate_by = 10

    def get_queryset(self):
        return Original_Task.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class Original_TaskDetailView(generic.DetailView):
    model = Original_Task

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather

class Original_TaskCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Original_Task
    fields = ['otask']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class Original_TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Original_Task
    fields = ['otask']

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class Original_TaskDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Original_Task
    success_url = reverse_lazy('original_tasks')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather








## Task Views

class CompletedTaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Task
    paginate_by = 10
    template_name = "parent/completed_task_list.html"

    def get_queryset(self):
        return Task.objects.filter(parent__user=self.request.user, status='COMP')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class TaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Task
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(parent__user=self.request.user)



    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Task
    fields = ['name', 'description', 'point_value', 'child', 'date']

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)
        return super().form_valid(form)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "parent/task_form.html"

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather






# Child Views

class ChildListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Child
    paginate_by = 10

    def get_queryset(self):
        return Child.objects.filter(parent__user=self.request.user)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class ChildDetailView(generic.DetailView):
    model = Child

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather




class ChildCreate(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Child
    form_class = ChildUpdateForm
    template_name = "parent/child_form.html"

    def form_valid(self, form):
        form.instance.parent = Parent.objects.get(user=self.request.user)

        return super().form_valid(form)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class ChildUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Child
    form_class = ChildUpdateForm
    template_name = "parent/child_form.html"

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class ChildDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Child
    success_url = reverse_lazy('children')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



# Parent Views


class ParentListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Parent
    paginate_by = 10

    def get_queryset(self):
        return Parent.objects.filter(user=self.request.user)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class ParentDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Parent

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


class ParentUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Parent
    fields = ['zip_code']

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    model = Parent
    form_class = UpdateProfileForm
    template_name = "parent/update_profile_form.html"
    success_url = reverse_lazy('settings')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['parent'] = parent = Parent.objects.get(user = self.request.user)
        return data

    def post(self, request, *args, **kwargs):

        zip_code = request.POST.get('zip_code')
        parent = Parent.objects.get(user = self.request.user)
        parent.zip_code = zip_code
        parent.save()

        return redirect('settings')


    def test_func(self):
        return self.request.user.is_active == True

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



class ParentDelete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Parent
    success_url = reverse_lazy('home')

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


# No Login Required




def home(request):
    return render(request, "parent/index.html")



class ParentSignUpView(View):
    form_class = ParentSignUpForm
    template_name = 'parent/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():

            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Kiddy-Up Account'
            message = render_to_string('parent/auth_user_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please confirm your email to complete registration.'))

            return redirect('login-redirect')

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been confirmed.'))
            return redirect('dashboard')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')




# Settings


class SettingsView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'parent/settings.html'

    def parent(self):
        return Parent.objects.get(user = self.request.user)
    def rewards(self):
        parent = Parent.objects.get(user = self.request.user)
        return Reward.objects.filter(parent=parent)
    def tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        return Task.objects.filter(parent=parent)
    def children(self):
        parent = Parent.objects.get(user = self.request.user)
        return Child.objects.filter(parent = parent)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


# Child Login Page (New)
def pre_child_login(request):
    parent = Parent.objects.get(user = request.user)
    parent.active_child = None
    parent.save()
    print(f'\n\nPARENT: {parent}\n\n', file=sys.stderr)
    print(f'\n\nACTIVE_CHILD: {parent.active_child}\n\n', file=sys.stderr)
    children = Child.objects.filter(parent = parent)
    for child in children:
        print(f'\n\nCHILD: {child.is_authenticated}\n\n', file=sys.stderr)
        child.is_authenticated = False
        child.save()
    return redirect('child_login')


class ChildLoginView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'parent/child_login.html'
    # form_class = ChildLoginForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['parent'] = parent = Parent.objects.get(user = self.request.user)
        data['children'] = Child.objects.filter(parent=parent)
        data['active_child'] = parent.active_child
        print(f'\n\nDEBUG: Parent = {parent}\n\n', file=sys.stderr)
        print(f'\n\nDEBUG: Active Child = {parent.active_child}\n\n', file=sys.stderr)
        if parent.active_child:
            child = parent.active_child
            data['pin'] = pin = child.pin
            print(f'\n\nDEBUG: PIN = {pin}\n\n', file=sys.stderr)
        return data


    def post(self, request, *args, **kwargs):
        pin_guess = request.POST.get('form_pin')
        # form = ChildLoginForm(request.POST)
        parent = Parent.objects.get(user = self.request.user)
        active_child = Child.objects.get(id = parent.active_child_id)
        if pin_guess == active_child.pin:

            #active_child = form.cleaned_data['id']
            # and pin entered is child pin
            children = Child.objects.filter(parent__user = self.request.user)
            for child in children:

                child.is_authenticated = False
                child.save()

            active_child.is_authenticated = True
            active_child.save()

            return redirect('child-dashboard')
        else:
            return redirect('child_login')
        return render(request, self.template_name)

    def test_func(self):
        return is_member(self.request.user)

    def weather(self):
        parent = Parent.objects.get(user = self.request.user)
        zip_code = '90210'
        if parent.zip_code:
            zip_code = parent.zip_code

        now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'

        day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the JSON to Python data types

        if day_weather['cod'] == '404':
            zip_code = '90210'
            now_url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=364040ff415088d88d047754583f0a7a'
            day_weather = requests.get(now_url.format(zip_code)).json() #request the API data and convert the

        city = day_weather['name']
        now_temp = day_weather['main']['feels_like']
        min_temp = day_weather['main']['temp_min']
        max_temp = day_weather['main']['temp_max']
        description = day_weather['weather'][0]['description']
        icon = day_weather['weather'][0]['icon']


        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather


def SetActiveChildView(request, pk):
    parent = Parent.objects.get(user = request.user)
    print(f'\n\nDEBUG: Parent = {parent}\n\n', file=sys.stderr)
    child = Child.objects.get(id = pk)
    print(f'\n\nDEBUG: Child = {child}\n\n', file=sys.stderr)
    parent.active_child = child
    print(f'\n\nDEBUG: Active Child = {parent.active_child}\n\n', file=sys.stderr)
    parent.save()
    return redirect('child_login')


def CheckPinView(request, pk):
    parent = Parent.objects.get(user = request.user)
    print(f'\n\nDEBUG: Parent = {parent}\n\n', file=sys.stderr)
    child = Child.objects.get(id = pk)
    print(f'\n\nDEBUG: Child = {child}\n\n', file=sys.stderr)
    parent.active_child = child
    print(f'\n\nDEBUG: Active Child = {parent.active_child}\n\n', file=sys.stderr)
    parent.save()
    return redirect('child_login')






# Child Views

class ChildDashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'parent/child_dashboard.html'

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def rewards(self):
        parent = Parent.objects.get(user = self.request.user)
        return Reward.objects.filter(parent = parent)

    def tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Task.objects.filter(child = active_child, status='OPEN')

    def completed_tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Task.objects.filter(child = active_child, status='COMP')

    def pending_tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Task.objects.filter(child = active_child, status='PEND')

    def earned_rewards(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Earned_Reward.objects.filter(child=active_child)


    def weather(self):
        current_weather = get_weather(self.request)

        city = current_weather['name']
        now_temp = current_weather['main']['feels_like']
        min_temp = current_weather['main']['temp_min']
        max_temp = current_weather['main']['temp_max']
        description = current_weather['weather'][0]['description']
        icon = current_weather['weather'][0]['icon']

        weather = {
            'city': city,
            'now_temp': now_temp,
            'min_temp': min_temp,
            'max_temp': max_temp,
            'description': description,
            'icon': icon
        }

        return weather



    def weather_help(self):

        current_weather = get_weather(self.request)

        max_temp = current_weather['main']['temp_max']
        description = current_weather['weather'][0]['description']
        icon = current_weather['weather'][0]['icon']

        notRain = True
        rainBoolean = "rain" in description
        if rainBoolean == True:
            notRain =False
        if max_temp > 80 and rainBoolean == True:
            help_image = "weather/greenumbrella.png"
        elif max_temp > 80 and rainBoolean == False:
            help_image = "weather/hotTemperature.png"
        elif max_temp > 55 and max_temp <= 80 and rainBoolean == True:
            help_image = "weather/greenumbrella.png"
        elif max_temp > 55 and max_temp <= 80 and rainBoolean == False:
            help_image = "weather/mild.jpg"
        elif max_temp <= 55  and rainBoolean == True:
            help_image = "weather/coldRain.png"
        elif max_temp <= 55  and rainBoolean == False:
            help_image = "weather/Cold.jpg"

        weather_help = {
            'icon': icon,
            'max_temp': max_temp,
            'help_image': help_image
        }

        return weather_help

    def test_func(self):
        return self.request.user.is_active == True





class ChildProfileView(generic.TemplateView):
    model = Child
    template_name = 'parent/child_profile.html'

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def test_func(self):
        return self.request.user.is_active == True




class ChildUpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Child
    form_class = ChildUpdateProfileForm
    template_name = "parent/child_update_profile_form.html"
    success_url = reverse_lazy('child-dashboard')


    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def test_func(self):
        return self.request.user.is_active == True


class ChildTaskListView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    model=Task
    template_name = 'parent/child_task_list.html'
    paginate_by = 10

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Task.objects.filter(child = active_child, status='OPEN')

    def completed_tasks(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Task.objects.filter(child = active_child, status='COMP')

    def test_func(self):
        return self.request.user.is_active == True

class ChildRewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    model=Reward
    template_name = 'parent/child_reward_list.html'
    paginate_by = 10

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def rewards(self):
        parent = Parent.objects.get(user = self.request.user)
        return Reward.objects.filter(parent=parent)

    def test_func(self):
        return self.request.user.is_active == True


class ChildTaskDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Task
    template_name = 'parent/child_task.html'

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def test_func(self):
        return self.request.user.is_active == True


class ChildRewardDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Reward
    template_name = 'parent/child_reward.html'

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def test_func(self):
        return self.request.user.is_active == True

def ChildRewardBuyView(request, pk):
    reward = Reward.objects.get(id=pk)
    parent = Parent.objects.get(user = request.user)
    active_child = parent.active_child
    reward_system.purchase_reward(active_child, reward)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def TaskCompleteView(request, pk):
    parent = Parent.objects.get(user = request.user)
    active_child = parent.active_child
    task = Task.objects.get(id=pk)
    reward_system.complete_task(active_child, task)
    # return redirect('child-tasks')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def TaskValidate(request, pk):
    task = Task.objects.get(id=pk)
    reward_system.parent_validate_task(task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def TaskInvalidate(request, pk):
    task = Task.objects.get(id=pk)
    reward_system.parent_invalidate_task(task)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ChildEarnedRewardListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model=Earned_Reward
    paginate_by = 10
    template_name = 'parent/child_earned_reward_list.html'

    def child(self):
        parent = Parent.objects.get(user = self.request.user)
        return parent.active_child

    def get_queryset(self):
        parent = Parent.objects.get(user = self.request.user)
        active_child = parent.active_child
        return Earned_Reward.objects.filter(child=active_child)

    def test_func(self):
        return is_member(self.request.user)
