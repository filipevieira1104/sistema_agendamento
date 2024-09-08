from django.contrib import admin
from .models import Especialidades, DadosBarbeiro, DatasAbertas, Valores, Servicos
from django.http import HttpResponseRedirect
from .views import gerar_relatorio_pdf, gerar_relatorio_excel
from django.urls import reverse, path

class ServicosAdmin(admin.ModelAdmin):
    list_display = ('servicos', 'valores')

class DadosBarbeiroAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na listagem
    list_display = ('nome', 'user', 'cep', 'bairro', 'especialidade', 'barbeiro_ativo')
    
    # Campos que podem ser usados como filtro lateral
    list_filter = ('bairro', 'especialidade', 'barbeiro_ativo')
    
    # Campos que podem ser buscados
    search_fields = ('nome', 'cep', 'bairro', 'user__username')
    
    # Ordenação padrão dos registros
    ordering = ('nome',)
    
    # Campos que aparecerão na página de edição, organizados em seções
    fieldsets = (
        (None, {
            'fields': ('nome', 'user', 'foto', 'barbeiro_ativo')
        }),
        ('Endereço', {
            'fields': ('cep', 'rua', 'numero', 'bairro')
        }),
        ('Informações Adicionais', {
            'fields': ('descricao', 'especialidade')
        }),
    )

    
    
    # Campos que serão exibidos como apenas leitura
    readonly_fields = ('user',)

    # Ações para gerar relatórios
    actions = ['exportar_relatorio_pdf', 'exportar_relatorio_excel']

    def exportar_relatorio_pdf(self, request, queryset=None):
        return HttpResponseRedirect(reverse('admin:gerar_relatorio_pdf'))

    def exportar_relatorio_excel(self, request, queryset=None):
        return HttpResponseRedirect(reverse('admin:gerar_relatorio_excel'))

    exportar_relatorio_pdf.short_description = "Exportar Relatório PDF"
    exportar_relatorio_excel.short_description = "Exportar Relatório Excel"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('gerar-relatorio-pdf/', self.admin_site.admin_view(gerar_relatorio_pdf), name='gerar_relatorio_pdf'),
            path('gerar-relatorio-excel/', self.admin_site.admin_view(gerar_relatorio_excel), name='gerar_relatorio_excel'),
        ]
        return custom_urls + urls
    
    

class DatasAbertasAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na listagem
    list_display = ('data', 'user', 'agendado')
    
    # Campos que podem ser usados como filtro lateral
    list_filter = ('agendado', 'data')
    
    # Campos que podem ser buscados
    search_fields = ('user__username', 'data')
    
    # Ordenação padrão dos registros
    ordering = ('-data',)  # Ordena pela data em ordem decrescente
    
    # Campos que aparecerão na página de edição, organizados em seções
    fieldsets = (
        (None, {
            'fields': ('data', 'user', 'agendado')
        }),
    )
    
    # Campos que serão exibidos como apenas leitura (se necessário)
    readonly_fields = ('data',)  # Por exemplo, se você não quiser que a data seja editável



admin.site.register(Especialidades, )
admin.site.register(DadosBarbeiro, DadosBarbeiroAdmin)
admin.site.register(DatasAbertas, DatasAbertasAdmin)
admin.site.register(Valores)
admin.site.register(Servicos, ServicosAdmin)