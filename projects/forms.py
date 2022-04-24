from django import forms
from django.contrib.auth.forms import UserCreationForm

from justwrite.settings import file_intro
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'file')



    def file_check(self, file, name):
        if file is None:
            print("a")
            f = open(name, "w")
            f.write(file_intro)
            f.close()
            return f
        elif file is not None:
            print("B")
            return file

        else:
            print("Error: file_check projects/forms.py")

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user

        if project.file is None:
            f = open(form.name, "w")
            f.write(file_intro)
            project.file = f
            print("Null!")
        elif project.file is not None:
            project.file = project.file
            print("not null?")

        else:
            print("Error: file_check projects/forms.py")

        form.save()