from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
import sys
from parent.models import Parent, Child, Task, Reward

from django.contrib.auth.models import User


class ParentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class ParentSignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row=u'<p style=" margin-left: 15px" %(html_class_attr)s>  %(label)s%(field)s</p> <p style=" margin-left: 37px;"%(help_text)s</p> <br/>',
            error_row=u'%s',
            row_ender='</p>',
            help_text_html=u' <span style=" opacity: 0.5;" class="helptext">%s</span>',
            errors_on_separate_row=True)

    @transaction.atomic
    def save(self):
        new_user = super().save(commit=False)
        new_user.is_parent = True
        new_user.save()
        parent = Parent.objects.create(user=new_user)
        return new_user


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Parent
        fields = ['zip_code']

    def __init__(self, user=None, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)


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

    def __init__(self, user, *args, **kwargs):
        super(ChildUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['target_reward'].queryset = Reward.objects.filter(parent__user=user)


class ChildUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['pin', 'target_reward', 'avatar']

    def __init__(self, user, *args, **kwargs):
        super(ChildUpdateProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['target_reward'].queryset = Reward.objects.filter(parent__user=user)

        #     self.fields['target_reward'].choices = Reward.objects.filter(parent__user = user)


class TaskCreateForm(forms.ModelForm):

    class Meta:

        model = Task
        fields = ['name', 'description', 'status', 'point_value', 'child', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):

        super(TaskCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['child'].queryset = Child.objects.filter(parent__user=user)
        else:
            print("user not found", file=sys.stderr)


class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'point_value', 'child', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):

        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['child'].queryset = Child.objects.filter(parent__user=user)
        else:
            print("user not found", file=sys.stderr)


class ChildLoginForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = ['pin']

    def __init__(self, user=None, *args, **kwargs):
        super(ChildLoginForm, self).__init__(*args, **kwargs)
