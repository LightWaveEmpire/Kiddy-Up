# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import RegisterForm


# Create your views here.
def home(request):
    return render(request, "parent/index.html")

def parent(request):
    return render(request, "parent/parent_dashboard.html")

def profile(request):
    return render(request, "parent/parent_profile.html")

def settings(request):
    return render(request, "parent/parent_settings.html")

