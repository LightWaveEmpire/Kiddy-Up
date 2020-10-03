# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import ParentCreationForm
from django.urls import reverse




# Require Login

@login_required
def home(request):
    return render(request, "parent/index.html")

@login_required
def parent(request):
    return render(request, "parent/parent_dashboard.html")

@login_required
def profile(request):
    return render(request, "parent/parent_profile.html")

@login_required
def settings(request):
    return render(request, "parent/parent_settings.html")


# Create your views here.

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
            return redirect(reverse("home"))
