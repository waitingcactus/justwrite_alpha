from django.db import models

from users.models import User


class Project(models.FileField):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
