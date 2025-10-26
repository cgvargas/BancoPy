from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Cliente, Conta, Transacao, ChavePix
from .forms import ClienteForm, ContaForm, DepositoForm, SaqueForm, TransferenciaForm, ChavePixForm, PixForm
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


def cadastrar_chave_pix(request, pk):
    """View para cadastrar chave PIX"""
    conta = get_object_or_404(Conta, pk=pk)

    if request.method == 'POST':
        form = ChavePixForm(request.POST)
        if form.is_valid():
            try:
                chave_pix = form.save(commit=False)
                chave_pix.conta = conta

                # Se for chave aleatoria, gerar automaticamente
                if chave_pix.tipo_chave == 'ALEATORIA':
                    chave_pix.chave = ChavePix.gerar_chave_aleatoria()

                chave_pix.save()
                messages.success(request, f'Chave PIX cadastrada com sucesso: {chave_pix.chave}')
                return redirect('listar_chaves_pix', pk=conta.numero)
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar chave PIX: {str(e)}')
    else:
        form = ChavePixForm()

    return render(request, 'contas/cadastrar_chave_pix.html', {'form': form, 'conta': conta})


def listar_chaves_pix(request, pk):
    """View para listar chaves PIX de uma conta"""
    conta = get_object_or_404(Conta, pk=pk)
    chaves = conta.chaves_pix.all()

    return render(request, 'contas/listar_chaves_pix.html', {'conta': conta, 'chaves': chaves})


def efetuar_pix(request, pk):
    """View para efetuar transferencia via PIX"""
    conta = get_object_or_404(Conta, pk=pk)

    if request.method == 'POST':
        form = PixForm(request.POST)
        if form.is_valid():
            chave_pix = form.cleaned_data['chave_pix']
            valor_str = form.cleaned_data['valor']
            # Substitui virgula por ponto
            valor_str = valor_str.replace(',', '.')
            valor = Decimal(valor_str)

            sucesso, mensagem, conta_destino = conta.transferir_pix(chave_pix, valor)

            if sucesso:
                # Registra a transacao
                Transacao.objects.create(
                    conta=conta,
                    tipo='P',
                    valor=valor,
                    conta_destino=conta_destino,
                    chave_pix=chave_pix,
                    descricao=f'PIX para {conta_destino.cliente.nome}'
                )
                messages.success(request, f'{mensagem} Destinatario: {conta_destino.cliente.nome}')
            else:
                messages.error(request, mensagem)

            return redirect('conta_detail', pk=conta.numero)
    else:
        form = PixForm()

    return render(request, 'contas/efetuar_pix.html', {'form': form, 'conta': conta})


def desativar_chave_pix(request, pk, chave_id):
    """View para desativar uma chave PIX"""
    conta = get_object_or_404(Conta, pk=pk)
    chave = get_object_or_404(ChavePix, pk=chave_id, conta=conta)

    chave.ativa = False
    chave.save()
    messages.success(request, 'Chave PIX desativada com sucesso!')

    return redirect('listar_chaves_pix', pk=conta.numero)
