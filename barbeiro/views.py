from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Especialidades, DadosBarbeiro, DatasAbertas
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime, timedelta
from clientes.models import Agendamentos
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.db.models import Count, Sum
import pandas as pd
import locale
from usuarios.models import CustomUser

@login_required
def cadastro_barbeiro(request):
    try:
        barbeiro_ativo = DadosBarbeiro.objects.get(user=request.user)
        if barbeiro_ativo.barbeiro_ativo:
            messages.add_message(request, constants.INFO, 'Você já possui um cadastro ativo')
            return redirect('/barbeiros/abrir_horario/')
    except:
        messages.add_message(request, constants.WARNING, 'Você precisa realizar seu cadastro de barbeiro')

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_barbeiro.html', {'especialidades': especialidades})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        foto = request.FILES.get('foto')
        descricao = request.POST.get('descricao')
        especialidade_id = request.POST.get('especialidade')

        # Busca a instância de Especialidades
        especialidade = get_object_or_404(Especialidades, id=especialidade_id)

        # Cria o objeto DadosBarbeiro com todos os dados necessários
        dados_barbeiro = DadosBarbeiro(
            user=request.user,  # Associa o barbeiro ao usuário autenticado
            nome=nome,
            cep=cep,
            rua=rua,
            numero=numero,
            bairro=bairro,
            foto=foto,
            descricao=descricao,
            especialidade=especialidade,
            barbeiro_ativo = True
        )
        dados_barbeiro.save()
        
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
        return redirect('/barbeiros/abrir_horario')

@login_required 
def abrir_horario(request):
    if not request.user.is_barbeiro:
          messages.add_message(request, constants.WARNING, 'Somente barbeiros podem acessar essa página!')
          return redirect('/usuarios/sair')
    
    if request.method == "GET":
        dados_barbeiro = DadosBarbeiro.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user)
        return render(request, 'abrir_horario.html', {'dados_barbeiro': dados_barbeiro, 'datas_abertas': datas_abertas})
    elif request.method == "POST":
        data = request.POST.get('data')
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data não pode ser anterior a data atual')
            return redirect('/barbeiros/abrir_horario/')
        
        horario_abrir = DatasAbertas(
            data=data,
            user=request.user,
        )
        horario_abrir.save()
        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso!')
        return redirect('/barbeiros/abrir_horario/')
    
def agendamentos_barbeiro(request):
    if not request.user.is_barbeiro:
        messages.add_message(request, constants.WARNING, 'Somente barbeiros podem acessar essa página!')
        return redirect('/usuarios/sair/')
    hoje = datetime.now().date()
    agendamentos_hoje = Agendamentos.objects.filter(datas_abertas__user=request.user).filter(datas_abertas__data__gte=hoje).filter(datas_abertas__data__lt=hoje + timedelta(days=1))
    agendamentos_restantes = Agendamentos.objects.exclude(id__in=agendamentos_hoje.values('id')).filter(datas_abertas__user=request.user)
    return render(request, 'agendamentos_barbeiro.html', {'agendamentos_hoje': agendamentos_hoje, 'agendamentos_restantes': agendamentos_restantes})

def agendamento_area_barbeiro(request, id_agendamento):
    if not request.user.is_barbeiro:
          messages.add_message(request, constants.WARNING, 'Somente barbeiros podem acessar essa página!')
          return redirect('/usuarios/sair')
    
    if request.method == "GET":
        agendamento = Agendamentos.objects.get(id=id_agendamento)
        cliente = CustomUser.objects.get(id=agendamento.cliente.id)
        return render(request, 'agendamento_area_barbeiro.html', {'agendamento': agendamento, 'cliente': cliente})
    
def finalizar_agendamento(request, id_agendamento):
    if not request.user.is_barbeiro:
      messages.add_message(request, constants.WARNING, 'Somente barbeiros podem acessar essa página!')
      return redirect('/usuarios/sair')
    
    agendamento = Agendamentos.objects.get(id=id_agendamento)
    if request.user != agendamento.datas_abertas.user:
        messages.add_message(request, constants.ERROR, 'Você não pode finalizar agendamento de outro barbeiro')
    agendamento.status = 'F'
    agendamento.save()
    return redirect(f'/barbeiros/agendamento_area_barbeiro/{id_agendamento}')
        
def gerar_relatorio_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_barbearia.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Título e Data
    pdf.setTitle("Relatório da Barbearia")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(200, height - 50, "Relatório da Barbearia")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 80, f"Data de geração: {timezone.now().strftime('%d/%m/%Y %H:%M')}")

    y = height - 120

    # Definir o local para português do Brasil
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Quantidade de Agendamentos
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Quantidade de Agendamentos")
    y -= 20
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    agendamentos_diarios = Agendamentos.objects.filter(datas_abertas__data__date=hoje).count()
    agendamentos_mensais = Agendamentos.objects.filter(datas_abertas__data__date__gte=primeiro_dia_mes, datas_abertas__data__date__lte=hoje).count()
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, y, f"Hoje ({hoje.strftime('%d/%m/%Y')}): {agendamentos_diarios}")
    y -= 20
    pdf.drawString(70, y, f"Mês Atual ({hoje.strftime('%B/%Y')}): {agendamentos_mensais}")
    y -= 40

    # Valor Total de Entrada
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Valor Total de Entrada")
    y -= 20
    valor_total = Agendamentos.objects.aggregate(total=Sum('total'))['total'] or 0
    pdf.setFont("Helvetica", 12)
    pdf.drawString(70, y, f"R$ {valor_total:.2f}")
    y -= 40

    # Quantidade de Atendimento por Barbeiro
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Quantidade de Atendimentos por Barbeiro")
    y -= 20
    atendimentos_barbeiros = Agendamentos.objects.values('datas_abertas__user__username').annotate(total=Count('id')).order_by('-total')

    data = [['Barbeiro', 'Quantidade de Atendimentos']]
    for atendimento in atendimentos_barbeiros:
        data.append([atendimento['datas_abertas__user__username'], atendimento['total']])

    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, y - (20 * len(data)))

    pdf.showPage()
    pdf.save()

    return response

def gerar_relatorio_excel(request):
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    agendamentos_diarios = Agendamentos.objects.filter(datas_abertas__data__date=hoje).count()
    agendamentos_mensais = Agendamentos.objects.filter(datas_abertas__data__date__gte=primeiro_dia_mes, datas_abertas__data__date__lte=hoje).count()
    valor_total = Agendamentos.objects.aggregate(total=Sum('total'))['total'] or 0
    atendimentos_barbeiros = Agendamentos.objects.values('datas_abertas__user__username').annotate(total=Count('id')).order_by('-total')

    # Gerar o arquivo Excel usando pandas
    with pd.ExcelWriter('relatorio_barbearia.xlsx', engine='openpyxl') as writer:
        resumo_data = {
            'Descrição': ['Agendamentos Diários', 'Agendamentos Mensais', 'Valor Total de Entrada'],
            'Valor': [agendamentos_diarios, agendamentos_mensais, f'R$ {valor_total:.2f}']
        }
        df_resumo = pd.DataFrame(resumo_data)
        df_resumo.to_excel(writer, sheet_name='Resumo', index=False)

        df_barbeiros = pd.DataFrame(list(atendimentos_barbeiros))
        df_barbeiros.rename(columns={'datas_abertas__user__username': 'Barbeiro', 'total': 'Quantidade de Atendimentos'}, inplace=True)
        df_barbeiros.to_excel(writer, sheet_name='Atendimentos por Barbeiro', index=False)

    # Abrir o arquivo gerado para retornar como resposta HTTP
    with open('relatorio_barbearia.xlsx', 'rb') as excel:
        response = HttpResponse(excel.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=relatorio_barbearia.xlsx'
        return response

