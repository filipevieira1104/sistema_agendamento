from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import get_user_model
import re

User = get_user_model()

def cadastro(request):
    if request.method == "GET":
        return render(request, 'home.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        print(senha)

        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            messages.add_message(request, constants.WARNING, 'Nome e e-mail não podem estar vazios')
            return redirect('/')

        if len(senha) < 8:
            messages.add_message(request, constants.WARNING, 'A senha deve ter no mmínimo 8 caracteres')
            return redirect('/')
        
        if not re.search(r'[A-Z]', senha):
            messages.add_message(request, constants.WARNING, 'A senha deve conter pelo menos uma letra maiúscula')
            return redirect('/')
        
        if not re.search(r'[a-z]', senha):
            messages.add_message(request, constants.WARNING, 'A senha deve conter pelo menos uma letra minúscula')
            return redirect('/')
        
        if not re.search(r'\d', senha):
            messages.add_message(request, constants.WARNING, 'A senha deve conter pelo menos um número')
            return redirect('/')
        
        if not re.search(r'[!@#$%^&*()-_+=]', senha):
            messages.add_message(request, constants.WARNING, 'A senha deve conter pelo menos um caractere especial !')
            return redirect('/')
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'E-mail já cadastrado')

        try:
            User.objects.create_user(
                username=nome,
                whatsapp=phone,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
            return redirect('/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/')    

def login(request):
    if request.method == "GET":
        return render(request, 'home.html')
    elif request.method == "POST":
        username = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)
        
        if user is not None:  # Verifica se a autenticação foi bem-sucedida
            auth.login(request, user)  # Registra o usuário na sessão
            if user.is_barbeiro:
                return redirect('/barbeiros/cadastro_barbeiro/')
            else:
                return redirect('/clientes/search/')  
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/')


def sair(request):
    auth.logout(request)
    messages.add_message(request, constants.WARNING, 'Faça login novamente para acessar o sistema')
    return redirect('/')          