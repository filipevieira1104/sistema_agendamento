from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\(\d{2}\)\d{5}-\d{4}$',
    message="O número de telefone deve estar no formato: (11)99999-9999"
)

class CustomUser(AbstractUser):
    is_barbeiro = models.BooleanField(default=False)  # Define se o usuário é barbeiro
    whatsapp = models.CharField(validators=[phone_validator], max_length=14)

    def __str__(self):
        return self.username  # Retorna o nome de usuário como representação textual
