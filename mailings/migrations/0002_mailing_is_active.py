# Generated by Django 5.0 on 2024-01-30 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активность рассылки'),
        ),
    ]
