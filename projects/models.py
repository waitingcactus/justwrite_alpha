from django.db import models

from users.models import User
from .validators import validate_file_extension


def user_directory_path(instance, filename):
    return f'{instance.user}/{filename}'

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])

    def __str__(self):
        return self.name
