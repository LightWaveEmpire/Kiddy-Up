from django.contrib.auth.forms import UserCreationForm
from django import forms


class ParentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)





