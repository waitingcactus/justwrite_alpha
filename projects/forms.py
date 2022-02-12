from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'file')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        form.save()