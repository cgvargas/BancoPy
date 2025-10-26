from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cliente(models.Model):
    """Modelo para representar um cliente do banco"""
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, verbose_name='Nome')
    email = models.EmailField(unique=True, verbose_name='E-mail')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'


class Conta(models.Model):
    """Modelo para representar uma conta bancária"""
    numero = models.AutoField(primary_key=True)
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='conta',
        verbose_name='Cliente'
    )
    saldo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Saldo'
    )
    limite = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('100.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Limite'
    )
    data_abertura = models.DateTimeField(auto_now_add=True, verbose_name='Data de Abertura')

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['numero']

    def __str__(self):
        return f'Conta {self.numero} - {self.cliente.nome}'

    @property
    def saldo_total(self):
        """Calcula o saldo total (saldo + limite)"""
        return self.saldo + self.limite

    def depositar(self, valor):
        """Realiza um depósito na conta"""
        if valor > 0:
            self.saldo += Decimal(str(valor))
            self.save()
            return True, 'Depósito efetuado com sucesso!'
        return False, 'Erro ao efetuar depósito. Valor deve ser positivo!'

    def sacar(self, valor):
        """Realiza um saque na conta"""
        valor = Decimal(str(valor))
        if valor <= 0:
            return False, 'Valor do saque deve ser positivo!'

        if valor > self.saldo_total:
            return False, 'Saque não realizado. Saldo insuficiente!'

        if self.saldo >= valor:
            self.saldo -= valor
        else:
            # Usa parte do limite
            restante = valor - self.saldo
            self.saldo = Decimal('0.00')
            self.limite -= restante

        self.save()
        return True, 'Saque efetuado com sucesso!'

    def transferir(self, conta_destino, valor):
        """Realiza uma transferência para outra conta"""
        valor = Decimal(str(valor))

        if valor <= 0:
            return False, 'Valor da transferência deve ser positivo!'

        if valor > self.saldo_total:
            return False, 'Transferência não realizada. Saldo insuficiente!'

        # Debita da conta origem
        if self.saldo >= valor:
            self.saldo -= valor
        else:
            restante = valor - self.saldo
            self.saldo = Decimal('0.00')
            self.limite -= restante

        # Credita na conta destino
        conta_destino.saldo += valor

        self.save()
        conta_destino.save()

        return True, 'Transferência efetuada com sucesso!'


class Transacao(models.Model):
    """Modelo para registrar histórico de transações"""
    TIPO_CHOICES = [
        ('D', 'Depósito'),
        ('S', 'Saque'),
        ('T', 'Transferência'),
    ]

    conta = models.ForeignKey(
        Conta,
        on_delete=models.CASCADE,
        related_name='transacoes',
        verbose_name='Conta'
    )
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, verbose_name='Tipo')
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    conta_destino = models.ForeignKey(
        Conta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transferencias_recebidas',
        verbose_name='Conta Destino'
    )
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')
    descricao = models.TextField(blank=True, verbose_name='Descrição')

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data_hora']

    def __str__(self):
        return f'{self.get_tipo_display()} - R$ {self.valor} - {self.data_hora.strftime("%d/%m/%Y %H:%M")}'
