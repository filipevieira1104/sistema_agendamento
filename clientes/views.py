from django.shortcuts import render,redirect, get_object_or_404
from barbeiro.models import DadosBarbeiro, Especialidades, DatasAbertas, Servicos
from clientes.models import Agendamentos
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import logging

@login_required
def search(request):
    if request.method == "GET":
        barbeiro_filtrar = request.GET.get('barbeiro')
        especialidades_filtrar = request.GET.getlist('especialidades')
        barbeiros = DadosBarbeiro.objects.all()

        if barbeiro_filtrar:
            barbeiros = barbeiros.filter(nome__icontains=barbeiro_filtrar)
        if especialidades_filtrar:
            barbeiros = barbeiros.filter(especialidade_id__in=especialidades_filtrar)   

        especialidades = Especialidades.objects.all()  
        servicos = Servicos.objects.all() 
        return render(request, 'search.html', {'barbeiros': barbeiros, 'especialidades': especialidades, 'servicos': servicos})
    
def escolher_horario(request, id_dados_barbeiro):
    barbeiro = get_object_or_404(DadosBarbeiro, id=id_dados_barbeiro)
    horarios_disponiveis = DatasAbertas.objects.filter(user=barbeiro.user, agendado=False)

    if not horarios_disponiveis.exists():
        messages.add_message(request, constants.ERROR, 'Não há horários disponíveis para este barbeiro.')
        return redirect('search')  # Nome correto da view de busca, ajustado para o nome exato

    if request.method == "POST":
        data_id = request.POST.get('escolher_horario')
        servico_ids = request.POST.getlist('servicos')
        total = 0  # Inicializa o total

        if data_id and data_id.isdigit() and servico_ids:
            try:
                data_selecionada = DatasAbertas.objects.get(id=data_id)
            except DatasAbertas.DoesNotExist:
                messages.add_message(request, constants.ERROR, 'Horário selecionado não é válido.')
                return redirect(reverse('escolher_horario', args=[id_dados_barbeiro]))

            agendamento = Agendamentos(
                cliente=request.user,
                datas_abertas=data_selecionada,
                total=0  # Inicialmente 0, será atualizado abaixo
            )
            agendamento.save()

            # Adiciona os serviços ao agendamento e calcula o total
            for servico_id in servico_ids:
                try:
                    servico_selecionado = Servicos.objects.get(id=servico_id)
                    agendamento.servico.add(servico_selecionado)  # Adiciona o serviço ao agendamento
                    total += servico_selecionado.valores.valores  # Soma o valor do serviço
                except Servicos.DoesNotExist:
                    messages.add_message(request, constants.ERROR, 'Serviço selecionado não é válido.')
                    return redirect(reverse('escolher_horario', args=[id_dados_barbeiro]))

            agendamento.total = total  # Atualiza o total no agendamento
            agendamento.save()

            data_selecionada.agendado = True
            data_selecionada.save()

            messages.add_message(request, constants.SUCCESS, f'Horário agendado com sucesso! Total: R$ {total:.2f}')
            return redirect('meus_agendamentos')  # Redireciona corretamente para 'meus_agendamentos'
        else:
            messages.add_message(request, constants.ERROR, 'Erro ao tentar agendar. Certifique-se de selecionar um horário válido e pelo menos um serviço.')
            return redirect(reverse('escolher_horario', args=[id_dados_barbeiro]))

    else:
        return render(request, 'search.html', {'barbeiro': barbeiro, 'horarios_disponiveis': horarios_disponiveis})    
        
def meus_agendamentos(request):
    agendamentos = Agendamentos.objects.filter(cliente=request.user).order_by('-datas_abertas__data')
    return render(request, 'meus_agendamentos.html', {'agendamentos': agendamentos})        

def detalhes(request, id_detalhes):
    if request.method == "GET":
        agendamento = Agendamentos.objects.get(id=id_detalhes)
        dado_barbeiro = DadosBarbeiro.objects.get(user=agendamento.datas_abertas.user)
        return render(request, 'detalhes.html', {'agendamento': agendamento, 'dado_barbeiro': dado_barbeiro})
    
def cancelar_agendamento(request, id_agendamento):
    agendamento = Agendamentos.objects.get(id=id_agendamento)
    if request.user != agendamento.cliente:
        messages.add_message(request, constants.ERROR, 'Você não pode finalizar agendamento de outro barbeiro')

    # Liberar horário cancelado para o barbeiro novamente    
    agendamento.datas_abertas.agendado = False
    agendamento.datas_abertas.save()

    agendamento.status = 'C'
    agendamento.save()
    return redirect(f'/clientes/detalhes/{id_agendamento}')   

# Configurar o logger
logger = logging.getLogger(__name__)

def lembretes(request):
    hora_atual = timezone.now()
    proxima_hora = hora_atual + timedelta(hours=1)

    # Depuração para verificar os valores
    print(f"Hora Atual: {hora_atual}")
    print(f"Próxima Hora: {proxima_hora}")

    # Filtrar agendamentos que faltam menos de 1 hora para começar
    agendamentos_proximos = Agendamentos.objects.filter(
        datas_abertas__data__gte=hora_atual,
        datas_abertas__data__lte=proxima_hora,
        status='A'
    )

    # Depuração para exibir os agendamentos encontrados
    for agendamento in agendamentos_proximos:
        print(f"Agendamento: {agendamento}, Data: {agendamento.datas_abertas.data}")

    return render(request, 'search.html', {'agendamentos_proximos': agendamentos_proximos})