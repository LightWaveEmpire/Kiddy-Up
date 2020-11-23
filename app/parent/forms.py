from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction

from parent.models import Parent, Child, Task, User



class ParentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class ParentSignUpForm(UserCreationForm):
#    first_name = forms.CharField(label='First name')
#    last_name = forms.CharField(label='Last name')
#    email = forms.EmailField(help_text='A valid email address, please.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = 'username', 'email'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.save()
        parent = Parent.objects.create(user=user)
        return user



class ChildSignUpForm(UserCreationForm):
    name = forms.CharField()
    age = forms.IntegerField()
    comp_level = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = 'username', 'name', 'age', 'comp_level'



class ChildUpdateForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'pin', 'target_reward', 'age', 'comp_level', 'current_points']

    def __init__(self, user=None, *args, **kwargs):
        super(ChildUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['target_reward'].choices = Reward.objects.filter(parent__user = user)


class ChildUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['pin', 'target_reward', 'avatar']

    def __init__(self, user=None, *args, **kwargs):
        super(ChildUpdateProfileForm, self).__init__(*args, **kwargs)
        # if user:
        #     self.fields['target_reward'].choices = Reward.objects.filter(parent__user = user)



class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'point_value', 'child', 'date']

    def __init__(self, user=None, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['child'].choices = Child.objects.filter(parent__user = user)


class ChildLoginForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = ['pin']

    def __init__(self, user=None, *args, **kwargs):
        super(ChildLoginForm, self).__init__(*args, **kwargs)





