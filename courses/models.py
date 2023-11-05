from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/', verbose_name='Изображение', **NULLABLE)
    body = models.TextField(verbose_name='Описание')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    body = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lessons/', verbose_name='Изображение', **NULLABLE)
    video_url = models.URLField(max_length=200, verbose_name='Ссылка на видео', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
