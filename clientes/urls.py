from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('escolher_horario/<int:id_dados_barbeiro>', views.escolher_horario, name='escolher_horario'),
    path('meus_agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
    path('detalhes/<int:id_detalhes>', views.detalhes, name='detalhes'),
    path('cancelar_agendamento/<int:id_agendamento>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('lembretes/', views.lembretes, name='lembretes')
]