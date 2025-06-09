from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователей."""

    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='''Username can contain letters,
                           digits, and @/./+/-/_ characters only.'''
            ),
        ]
    )

    email = models.EmailField(db_index=True, max_length=254, unique=True, )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def __str__(self):
        return self.username
