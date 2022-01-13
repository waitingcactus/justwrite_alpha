from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
