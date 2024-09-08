from django.contrib import admin
from .models import Agendamentos

class AgendamentosAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'datas_abertas', 'status', 'total')  # Campos exibidos na listagem
    list_filter = ('status',)  # Filtros laterais
    search_fields = ('cliente__username',)  # Campo de busca
    ordering = ('datas_abertas',)  # Ordenação dos registros
    
    # Organizando os campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('cliente', 'datas_abertas', 'status')
        }),
        ('Serviços', {
            'fields': ('servico',),
        }),
        ('Financeiro', {
            'fields': ('total',)
        }),
    )
    
    # Personalizando a exibição de campos ManyToMany
    filter_horizontal = ('servico',)  # Exibe o campo 'servico' com um widget horizontal
admin.site.register(Agendamentos, AgendamentosAdmin)    
