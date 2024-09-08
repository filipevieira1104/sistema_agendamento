from django.urls import path, include
from . import views

urlpatterns = [
    path('cadastro_barbeiro/', views.cadastro_barbeiro, name='cadastro_barbeiro'),
    path('abrir_horario/', views.abrir_horario, name='abrir_horario'),
    path('agendamentos_barbeiro/', views.agendamentos_barbeiro, name='agendamentos_barbeiro'),
    path('agendamento_area_barbeiro/<int:id_agendamento>/', views.agendamento_area_barbeiro, name='agendamento_area_barbeiro'),
    path('finalizar_agendamento/<int:id_agendamento>/', views.finalizar_agendamento, name='finalizar_agendamento'),
    path('relatorio/pdf', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('relatorio/excel', views.gerar_relatorio_excel, name='gerar_relatorio_excel'),
]
