from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Defina os campos que deseja exibir no Django Admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_barbeiro')
    list_filter = ('is_barbeiro', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    # Defina quais campos são editáveis no formulário de criação/edição de usuários
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'whatsapp')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Status do Barbeiro', {'fields': ('is_barbeiro',)}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos exibidos ao adicionar um novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_barbeiro', 'whatsapp'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
