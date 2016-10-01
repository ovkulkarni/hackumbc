from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets


class AuthenticateForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticateForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(attrs={"placeholder": "Username", "class": "form-control"})
        self.fields["password"].widget = widgets.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        return form
