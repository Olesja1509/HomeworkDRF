from django.db import models

from courses.models import Course, Lesson
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Payment(models.Model):

    METHOD = (
        ('Cash', 'Наличные'),
        ('Card', 'Перевод на счет')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payment', **NULLABLE)
    date = models.CharField(max_length=20, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(max_length=20, choices=METHOD, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user}/{self.course if self.course else self.lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('date',)
