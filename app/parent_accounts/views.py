# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import RegisterForm


# Create your views here.
def home(request):
    return render(request, "parent_accounts/index.html")

def parent(request):
    return render(request, "parent_accounts/parent_dashboard.html")
