from django.contrib import admin
from django.urls import include, path
from . import views

#from django.conf import settings

urlpatterns = [
    path('about/', views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
]