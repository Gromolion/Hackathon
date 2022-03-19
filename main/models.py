from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название проекта')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Panel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название панели')
    project = models.ForeignKey('Project', db_index=True, on_delete=models.CASCADE, verbose_name='Проект')

    class Meta:
        verbose_name = 'Панель'
        verbose_name_plural = 'Панели'


class Info(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    panel = models.OneToOneField(Panel, on_delete=models.CASCADE)


class UserPanel(models.Model):
    user = models.ForeignKey('auth.User', db_index=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    panel = models.ForeignKey('Panel', db_index=True, on_delete=models.CASCADE, verbose_name='Панель')


class UserKeys(models.Model):
    user = models.OneToOneField('auth.User', db_index=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    publickey = models.BinaryField()
    secretkey_enc = models.BinaryField()
