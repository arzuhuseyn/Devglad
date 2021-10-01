from django.db import models

from django.contrib.auth.models import AbstractUser
from devglad.utils.base import BaseModel


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserProfile(BaseModel):
    USER_TYPES = (
        (1, 'Developer'),
        (2, 'Recruiter'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.IntegerField(choices=USER_TYPES, default=1)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user} - Profile'