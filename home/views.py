from django.shortcuts import render
from django.http import HttpResponse
from barbeiro.models import Servicos

def home(request):
    if request.method == "GET":
        servico = Servicos.objects.all()
        return render(request, 'home.html', {'servico': servico})