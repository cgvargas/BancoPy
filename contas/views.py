from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Cliente, Conta, Transacao
from .forms import ClienteForm, ContaForm, DepositoForm, SaqueForm, TransferenciaForm
from decimal import Decimal


def home(request):
    """View para página inicial"""
    total_contas = Conta.objects.count()
    total_clientes = Cliente.objects.count()
    context = {
        'total_contas': total_contas,
        'total_clientes': total_clientes,
    }
    return render(request, 'contas/home.html', context)


class ContaListView(ListView):
    """View para listar todas as contas"""
    model = Conta
    template_name = 'contas/conta_list.html'
    context_object_name = 'contas'
    paginate_by = 10


class ContaDetailView(DetailView):
    """View para detalhar uma conta específica"""
    model = Conta
    template_name = 'contas/conta_detail.html'
    context_object_name = 'conta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transacoes'] = self.object.transacoes.all()[:10]
        return context


def criar_conta(request):
    """View para criar uma nova conta"""
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            try:
                # Cria o cliente
                cliente = cliente_form.save()

                # Cria a conta para o cliente
                conta = Conta.objects.create(cliente=cliente)

                messages.success(request, f'Conta {conta.numero} criada com sucesso para {cliente.nome}!')
                return redirect('conta_detail', pk=conta.numero)
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
    else:
        cliente_form = ClienteForm()

    return render(request, 'contas/criar_conta.html', {'form': cliente_form})


def efetuar_deposito(request, pk):
    """View para efetuar depósito"""
    conta = get_object_or_404(Conta, pk=pk)

    if request.method == 'POST':
        form = DepositoForm(request.POST)
        if form.is_valid():
            valor_str = form.cleaned_data['valor']
            # Substitui vírgula por ponto
            valor_str = valor_str.replace(',', '.')
            valor = Decimal(valor_str)

            sucesso, mensagem = conta.depositar(valor)

            if sucesso:
                # Registra a transação
                Transacao.objects.create(
                    conta=conta,
                    tipo='D',
                    valor=valor,
                    descricao='Depósito em conta'
                )
                messages.success(request, mensagem)
            else:
                messages.error(request, mensagem)

            return redirect('conta_detail', pk=conta.numero)
    else:
        form = DepositoForm()

    return render(request, 'contas/deposito.html', {'form': form, 'conta': conta})


def efetuar_saque(request, pk):
    """View para efetuar saque"""
    conta = get_object_or_404(Conta, pk=pk)

    if request.method == 'POST':
        form = SaqueForm(request.POST)
        if form.is_valid():
            valor_str = form.cleaned_data['valor']
            # Substitui vírgula por ponto
            valor_str = valor_str.replace(',', '.')
            valor = Decimal(valor_str)

            sucesso, mensagem = conta.sacar(valor)

            if sucesso:
                # Registra a transação
                Transacao.objects.create(
                    conta=conta,
                    tipo='S',
                    valor=valor,
                    descricao='Saque em conta'
                )
                messages.success(request, mensagem)
            else:
                messages.error(request, mensagem)

            return redirect('conta_detail', pk=conta.numero)
    else:
        form = SaqueForm()

    return render(request, 'contas/saque.html', {'form': form, 'conta': conta})


def efetuar_transferencia(request, pk):
    """View para efetuar transferência"""
    conta_origem = get_object_or_404(Conta, pk=pk)

    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            numero_destino = form.cleaned_data['numero_conta_destino']
            valor_str = form.cleaned_data['valor']
            # Substitui vírgula por ponto
            valor_str = valor_str.replace(',', '.')
            valor = Decimal(valor_str)

            try:
                conta_destino = Conta.objects.get(numero=numero_destino)

                if conta_origem.numero == conta_destino.numero:
                    messages.error(request, 'Não é possível transferir para a mesma conta!')
                else:
                    sucesso, mensagem = conta_origem.transferir(conta_destino, valor)

                    if sucesso:
                        # Registra a transação
                        Transacao.objects.create(
                            conta=conta_origem,
                            tipo='T',
                            valor=valor,
                            conta_destino=conta_destino,
                            descricao=f'Transferência para conta {conta_destino.numero}'
                        )
                        messages.success(request, mensagem)
                    else:
                        messages.error(request, mensagem)

                return redirect('conta_detail', pk=conta_origem.numero)
            except Conta.DoesNotExist:
                messages.error(request, f'Conta {numero_destino} não encontrada!')
    else:
        form = TransferenciaForm()

    return render(request, 'contas/transferencia.html', {'form': form, 'conta': conta_origem})
