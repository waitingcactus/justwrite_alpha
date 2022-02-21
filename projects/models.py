import os

import tinymce
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.forms.fields import *

from users.models import User
from .validators import validate_file_extension
import decimal
import string

import re, cgi
tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

def user_directory_path(instance, filename):
    path = f'files/{instance.user}/'
    ext = os.path.splitext(filename)[1]
    format = instance.name + ext
    return os.path.join(path, format)

def user_directory_path_local(user, filename):
    return f'files/{user}/{filename}'


class Project(models.Model):

    COUNT_OPTIONS = [
        ('Words', (
                ('50W','50 Words'),
                ('100W', '100 Words'),
                ('200W', '200 Words'),
                ('500W', '500 Words'),
                ('1000W', '1000 Words'),
            )
        ),
        ('Time', (
              ('10M', '10 Minutes'),
              ('20M', '20 Minutes'),
              ('30M', '30 Minutes'),
              ('60M', '1 hour'),
              ('120M', '2 hours'),
          )
        ),
    ]

    PROGRESS_TYPES = (
        ('Automatic', 'Automatic'),
        ('manual', 'Manual')
    )

    worddict = {

        "50W":50,
        "100W": 100,
        "200W": 200,
        "500W": 500,
        "1000W": 1000
    }

    timedict = {

        "10M": 10,
        "20M": 20,
        "30M": 30,
        "60M": 60,
        "120M": 120
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path, validators=[validate_file_extension])
    goal = models.CharField(max_length=10, choices=COUNT_OPTIONS, default='50W', null=True)
    goalProgress = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True)
    progressTracker = models.CharField(max_length=9, choices=PROGRESS_TYPES, default='Automatic')

    fileContentsBefore = "test! file data not retrieved or displayed"
    fileContentsCurrent = ""
    fileContentsAfter = ""

    def __str__(self):
        return self.name

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        try:
            with open(str(self.file.path)) as f:
                self.fileContentsBefore = "".join(f.readlines())

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
        #print(self.fileContentsCurrent)

    #data getters
    #sanatises model fields into form fields to support localisation e.g. maths

    def get_goal_progress(self):

        #return #float('{}'.format(self.goalProgress))
        return self.goalProgress

    def get_streak(self):
        return int(self.goalProgress)

    def get_word_count(self, data):
        no_tags = tag_re.sub('',data)
        no_nbsp = no_tags.replace("&nbsp"," ")
        word_count = sum(word.strip(string.punctuation).isalpha() for word in no_nbsp.split())
        return word_count


    #progress setter
    def set_streak(self, data):
        if "W" in self.goal:
            self.goalProgress = self.get_word_count(data)/self.worddict[self.goal]

        elif "M" in self.goal:
            self.goalProgress = data / self.timedict[self.goal]

        else:
            print("error in goal_type set_streak function")





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
