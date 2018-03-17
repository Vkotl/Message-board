from django import forms
from django.contrib.auth import authenticate
from .models import User

# A form that will be used in the login screen.
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    # Is called by .is_valid() and will return a dictionary(cleaned_data) of form members name and their values.
    def clean(self):
        # Check if both username and password are filled in the form.
        if all(key in self.cleaned_data for key in ('username', 'password')):
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            # Authenticate the username and password and then return cleaned_data.
            user = authenticate(username=username, password=password)
            if user is not None:
                return self.cleaned_data
        raise forms.ValidationError(r"Username and password are incorrect.")


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    pass_repeat = forms.CharField(widget=forms.PasswordInput(), label='Password again:')

    # Is called by .is_valid() and will return a dictionary(cleaned_data) of form members name and their values.
    def clean(self):
        # Check if username, password and pass_repeat are filled in the form.
        if all(key in self.cleaned_data for key in ('username', 'password', 'pass_repeat')):
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            pass_repeat = self.cleaned_data['pass_repeat']
            # Make sure both passwords are the same.
            if password != pass_repeat:
                raise forms.ValidationError(r"Passwords do not match.")
            # Make sure that the username doesn't exist already.
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(r"Username already used.")
            # If all passed then send the form data.
            return self.cleaned_data
        raise forms.ValidationError(r"Some of the fields were left empty.")


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea({'cols': 30, 'rows': 3}), label=False)

    # Is called by .is_valid() and will return a dictionary(cleaned_data) of form members name and their values.
    def clean(self):
        # If a message was written into the textarea then content will exist, otherwise it will not.
        if 'content' in self.cleaned_data:
            return self.cleaned_data
        raise forms.ValidationError(r"Must have text to send.")