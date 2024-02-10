from django.db import models
import users.models
from django.utils import timezone

import users

STATUS_CHOICES = [
    ('Создана', 'Создана'),
    ('Запущена', 'Запущена'),
    ('Завершена', 'Завершена'),
]
INTERVAL_CHOICES = [
    ('разовая', 'разовая'),
    ('ежедневно', 'ежедневно'),
    ('раз в неделю', 'раз в неделю'),
    ('раз в месяц', 'раз в месяц'),
]

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель Клиента
    """
    full_name = models.CharField(max_length=50, verbose_name='ФИО')
    email = models.EmailField(max_length=50, verbose_name='Email')
    comment = models.CharField(max_length=300, verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='взаимодействует с клиентом')

    def __str__(self):
        return f'{self.full_name}- {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    """
    Модель сообщения
    """
    title = models.CharField(max_length=250, verbose_name='тема')
    content = models.TextField(verbose_name='содержание', **NULLABLE)

    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец сообщения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    """
    Модель рассылки
    """
    name = models.CharField(max_length=50, verbose_name='название рассылки', **NULLABLE)
    mail_to = models.ManyToManyField(Client, verbose_name='кому')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)
    data_mailing = models.DateTimeField(default=timezone.now, verbose_name='Время рассылки')
    periodicity = models.CharField(default='разовая', max_length=50, choices=INTERVAL_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, help_text="Выберите Создана или Завершена")
    is_activated = models.BooleanField(default=True, verbose_name='активная рассылка')

    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, verbose_name='Владелец рассылки')

    def __str__(self):
        return f'{self.data_mailing}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('set_is_activated', 'Может отключать рассылку')
        ]


class Logs(models.Model):
    """
    Модель Logs
    """
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)
    last_mailing_time = models.DateTimeField(auto_now=True, verbose_name='время последней рассылки')
    status = models.CharField(max_length=50, verbose_name='статус попытки', null=True)

    def __str__(self):
        return f'Отправлено: {self.last_mailing_time}, ' \
               f'Статус: {self.status}'

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'

