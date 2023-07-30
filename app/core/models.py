
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


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
