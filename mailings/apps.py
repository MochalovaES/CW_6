from django.apps import AppConfig


class SendmailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailings'
    verbose_name = 'Рассылки'