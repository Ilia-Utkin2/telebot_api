from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Менеджер для модели пользователей."""

    def create_user(
        self,
        username,
        email,
        password,
    ):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        if password is None:
            raise TypeError('Users must have a password.')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        password=None
    ):
        """Создает и возвращает пользователя с привилегиями суперадмина."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username,
            email,
            password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
