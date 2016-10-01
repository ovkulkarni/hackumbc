from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets

from .models import User


class AuthenticateForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticateForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(attrs={"placeholder": "Username", "class": "form-control"})
        self.fields["password"].widget = widgets.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        return form


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32, widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email Address", "class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=64, widget=forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=64, widget=forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"}))

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
