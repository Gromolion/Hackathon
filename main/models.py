from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255, verbose_name='Папка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папка'


class Access(models.Model):
    name = models.CharField(max_length=255, verbose_name='Доступ')
    value = models.CharField(max_length=255, verbose_name='Значение')
    folder = models.ForeignKey('Folder', db_index=True, on_delete=models.CASCADE, verbose_name='Папка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'


class UserAccess(models.Model):
    user = models.ForeignKey('auth.User', db_index=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    access = models.ForeignKey('Access', db_index=True, on_delete=models.CASCADE, verbose_name='Доступ')


class UserKeys(models.Model):
    user = models.OneToOneField('auth.User', db_index=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    public_key = models.TextField(verbose_name='Публичный')
    private_key = models.TextField(verbose_name='Секретный')


class UserAdmin(models.Model):
    folder = models.ForeignKey('Folder', db_index=True, on_delete=models.CASCADE, verbose_name='Папка')
    user = models.OneToOneField('auth.User', db_index=True, on_delete=models.CASCADE, verbose_name='Пользователь')
