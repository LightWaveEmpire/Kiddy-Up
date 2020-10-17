# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from about.forms import ContactForm
from django.views.generic.edit import FormView


# Create views here.

# Require Login

def about(request):
    return render(request, "about/about.html")

#def contact(request):
#    return render(request, "about/contact.html")

def faq(request):
    return render(request, "about/faq.html")


class ContactForm(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
