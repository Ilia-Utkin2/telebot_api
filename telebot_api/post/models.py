from constants import MAX_TITLE
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Выберите автора рецепта'
    )
    title = models.CharField(
        max_length=MAX_TITLE,
        verbose_name='Название поста',
        help_text='Введите название поста'
    )
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
