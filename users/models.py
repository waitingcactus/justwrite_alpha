from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True, editable=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    streak = models.IntegerField(default=0)
    streak_cont = models.BooleanField(default=False)
    last_name_change = models.DateTimeField(verbose_name='last name change', auto_now=True)
    last_email_change = models.DateTimeField(verbose_name='last name change', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    country = CountryField(default='GB', blank_label='(Select country)')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser

    def name_changed_recently(self):
        time = timezone.now() - timezone.timedelta(days=30)
        return time < self.last_name_change

    def email_changed_recently(self):
        time = timezone.now() - timezone.timedelta(days=30)
        return time < self.last_email_change


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000)
    AVATAR_CHOICES = (
        ('profile_pics/turtle.jpg', 'turtle'),
        ('profile_pics/male.jpg', 'default man'),
        ('profile_pics/female.jpg', 'default woman'),
    )
    image = models.ImageField(default='profile_pics/turtle.jpg', choices=AVATAR_CHOICES)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('D', 'Prefer not to say'),
    )
    gender = models.CharField(default='D', max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.user} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


