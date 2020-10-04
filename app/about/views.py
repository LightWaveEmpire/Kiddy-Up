# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse



# Create views here.

# Require Login

def about(request):
    return render(request, "about/about.html")

def contact(request):
    return render(request, "about/contact.html")

def faq(request):
    return render(request, "about/faq.html")


