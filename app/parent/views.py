# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
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

