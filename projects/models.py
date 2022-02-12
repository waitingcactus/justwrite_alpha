import os
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse

from users.models import User
from .validators import validate_file_extension


def user_directory_path(instance, filename):
    path = f'files/{instance.user}/'
    ext = os.path.splitext(filename)[1]
    format = instance.name + ext
    return os.path.join(path, format)


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects', kwargs={'username': self.user})


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
