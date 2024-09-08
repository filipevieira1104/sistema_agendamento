from django.db import models
from django.conf import settings
from django.db.models import Q
from datetime import datetime

class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to='icones', null=True, blank=True)

    def __str__(self) -> str:
        return self.especialidade

class Valores(models.Model):
    valores = models.FloatField()

    def __str__(self) -> str:
        return str(self.valores)    
    
class Servicos(models.Model):
    servicos = models.CharField(max_length=100)
    valores = models.ForeignKey(Valores, on_delete=models.DO_NOTHING)    

    def __str__(self) -> str:
        return self.servicos    
    
class DadosBarbeiro(models.Model):
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos_perfil')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    descricao = models.TextField(null=True, blank=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)
    barbeiro_ativo = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.username 

    @property
    def proximas_datas_disponiveis(self):
        agora = datetime.now()
        # Filtra datas e horários futuros
        proximas_datas = DatasAbertas.objects.filter(
            Q(user=self.user) &
            Q(data__gt=agora) &
            Q(agendado=False)
        ).order_by('data')

        return proximas_datas
  
    
class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.data)
    


