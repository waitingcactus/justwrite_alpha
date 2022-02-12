from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput

from .models import User, Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'country')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'country')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.name_changed_recently():
            self.fields['username'].widget.attrs['readonly'] = True
        if self.instance.email_changed_recently():
            self.fields['email'].widget.attrs['readonly'] = True

    email = forms.EmailField(max_length=60, help_text='')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('word_target', 'gender', 'image')
