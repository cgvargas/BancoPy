# -*- coding: utf-8 -*-
from django import forms
from .models import Cliente, Conta, ChavePix


class ClienteForm(forms.ModelForm):
    """Formulario para cadastro de cliente"""
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data de Nascimento'
    )

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'cpf', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'cpf': 'CPF',
        }


class ContaForm(forms.ModelForm):
    """Formulario para conta"""
    class Meta:
        model = Conta
        fields = ['cliente']


class DepositoForm(forms.Form):
    """Formulario para deposito"""
    valor = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 100,50',
            'pattern': '[0-9]+([,\.][0-9]{1,2})?'
        }),
        label='Valor do Deposito (R$)',
        help_text='Use virgula ou ponto como separador decimal'
    )


class SaqueForm(forms.Form):
    """Formulario para saque"""
    valor = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 100,50',
            'pattern': '[0-9]+([,\.][0-9]{1,2})?'
        }),
        label='Valor do Saque (R$)',
        help_text='Use virgula ou ponto como separador decimal'
    )


class TransferenciaForm(forms.Form):
    """Formulario para transferencia"""
    numero_conta_destino = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numero da conta'
        }),
        label='Numero da Conta Destino'
    )
    valor = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 100,50',
            'pattern': '[0-9]+([,\.][0-9]{1,2})?'
        }),
        label='Valor da Transferencia (R$)',
        help_text='Use virgula ou ponto como separador decimal'
    )


class ChavePixForm(forms.ModelForm):
    """Formulario para cadastro de chave PIX"""
    class Meta:
        model = ChavePix
        fields = ['tipo_chave', 'chave']
        widgets = {
            'tipo_chave': forms.Select(attrs={'class': 'form-control'}),
            'chave': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua chave PIX'
            }),
        }
        labels = {
            'tipo_chave': 'Tipo de Chave',
            'chave': 'Chave PIX',
        }


class PixForm(forms.Form):
    """Formulario para transferencia via PIX"""
    chave_pix = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a chave PIX do destinatario'
        }),
        label='Chave PIX',
        help_text='CPF, E-mail, Telefone ou Chave Aleatoria'
    )
    valor = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 100,50',
            'pattern': '[0-9]+([,\.][0-9]{1,2})?'
        }),
        label='Valor do PIX (R$)',
        help_text='Use virgula ou ponto como separador decimal'
    )
