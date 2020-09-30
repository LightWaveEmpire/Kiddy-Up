# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from .forms import RegisterForm


# Create your views here.

def child(request):
    return render(request, "child/child_dashboard.html")
