
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from rest_framework import settings
from django.conf import settings


class UserManager(BaseUserManager):
    # manager for users

    # password=None to create dummy users without password
    # **other_fields will help to add more fields to user model without
    # needing to change create_user method
    def create_user(self, email, password=None, **other_fields):
        # create, save and return a new user
        # added normalise_email feature of baseUserManager class
        if not email:
            raise ValueError('Email not provided')
        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        # self._db to future proff when using multiple DBs
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """defauly User model in system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    link = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.title
