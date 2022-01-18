from django.db import models

from users.models import User


class Forest(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user}'s forest"

    def add_tree(self):
        Tree.objects.create(forest=self)


class Tree(models.Model):
    forest = models.ForeignKey(
        Forest,
        on_delete=models.CASCADE,
    )