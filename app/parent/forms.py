from django.contrib.auth.forms import UserCreationForm

class ParentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
