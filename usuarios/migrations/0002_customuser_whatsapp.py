# Generated by Django 5.1 on 2024-09-05 18:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='whatsapp',
            field=models.CharField(default=1, max_length=15, validators=[django.core.validators.RegexValidator(message='O número deve estar no formato: (11) 99999-9999', regex='^\\(\\d{2}\\)\\s\\d{5}-\\d{4}$')]),
            preserve_default=False,
        ),
    ]
