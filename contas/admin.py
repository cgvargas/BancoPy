from django.contrib import admin
from .models import Cliente, Conta, Transacao


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Administração de clientes"""
    list_display = ['codigo', 'nome', 'email', 'cpf', 'data_cadastro']
    list_filter = ['data_cadastro']
    search_fields = ['nome', 'email', 'cpf']
    readonly_fields = ['codigo', 'data_cadastro']
    ordering = ['nome']


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    """Administração de contas"""
    list_display = ['numero', 'get_cliente_nome', 'saldo', 'limite', 'saldo_total', 'data_abertura']
    list_filter = ['data_abertura']
    search_fields = ['numero', 'cliente__nome', 'cliente__cpf']
    readonly_fields = ['numero', 'data_abertura', 'saldo_total']
    ordering = ['numero']

    def get_cliente_nome(self, obj):
        return obj.cliente.nome
    get_cliente_nome.short_description = 'Cliente'
    get_cliente_nome.admin_order_field = 'cliente__nome'


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    """Administração de transações"""
    list_display = ['id', 'conta', 'tipo', 'valor', 'conta_destino', 'data_hora']
    list_filter = ['tipo', 'data_hora']
    search_fields = ['conta__numero', 'conta__cliente__nome']
    readonly_fields = ['data_hora']
    ordering = ['-data_hora']

    def has_add_permission(self, request):
        # Não permite adicionar transações manualmente pelo admin
        return False

    def has_change_permission(self, request, obj=None):
        # Não permite editar transações
        return False
