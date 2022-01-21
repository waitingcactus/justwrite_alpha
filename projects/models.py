import os

import tinymce
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse

from users.models import User
from .validators import validate_file_extension


def user_directory_path(instance, filename):
    return f'files/{instance.user}/{filename}'

def user_directory_path_local(user, filename):
    return f'files/{user}/{filename}'


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])

    fileContentsBefore = "test! file data not retrieved or displayed"
    fileContentsCurrent = ""
    fileContentsAfter = ""

    def __str__(self):
        return self.name

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        try:
            with open(str(self.file.path)) as f:
                self.fileContentsBefore = f.readlines()

        except:
            print("project constructor error")

    def get_absolute_url(self):
        return reverse('projects', kwargs={'username': self.user})

    def user_directory_path(instance, filename):
        path = f'files/{instance.user}/'
        ext = os.path.splitext(filename)[1]
        format = instance.name + ext
        return os.path.join(path, format)

    def set_file_contents(self, sessionInProgress):
        with open(str(self.file.path)) as f:
            self.fileContentsBefore = f.readlines()
        #if sessionInProgress == False:
        #    with open(str(self.file.path)) as f:
        #        self.fileContentsBefore = f.readlines()
        #elif sessionInProgress == True:
        #    self.fileContents = f.readlines()
        #fileContents = ""

    def submit_file_contents(self, data):
        print("submit called")
        f = open(self.file.path, "w")
        f.write(data)
        f.close()

    def save_file_contents(self, data):
        print("save called")
        self.fileContentsCurrent = data
        print(self.fileContentsCurrent)





@receiver(models.signals.post_delete, sender=Project)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when
    corresponding 'Project' is deleted
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Project)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Project` is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Project.objects.get(pk=instance.pk).file
    except Project.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
