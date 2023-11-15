from django import forms
from .models import CustomUser
from manga_info.models import Author


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'subscribers']


class ChangeAuthorForm(forms.ModelForm):
    old_name = forms.CharField(max_length=100)
    old_last = forms.CharField(max_length=100)

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'subscribers']

    field_order = ['old_name', 'old_last', 'first_name', 'last_name', 'subscribers']
