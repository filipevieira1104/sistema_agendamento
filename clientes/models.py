from django.db import models
from django.conf import settings
from barbeiro.models import DatasAbertas, Servicos

class Agendamentos(models.Model):
    status_choices = (
        ('A', 'Agendado'),
        ('C', 'Cancelado'),
        ('F', 'Finalizado')
    )
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    datas_abertas = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    servico = models.ManyToManyField(Servicos)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.cliente.username
