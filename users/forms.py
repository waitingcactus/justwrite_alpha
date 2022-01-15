from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput

from .models import User, Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.request.user.name_changed_recently():
            self.fields['username'].required = False
            self.fields['username'].widget.attrs['disabled'] = "disabled"
        if self.request.user.email_changed_recently():
            self.fields['email'].required = False
            self.fields['email'].widget.attrs['disabled'] = "disabled"

    email = forms.EmailField(max_length=60, help_text='')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'country', 'image')
