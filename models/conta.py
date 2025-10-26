from models.cliente import Cliente
from utils.helper import formata_float_str_moeda


class Conta:

    codigo: int = 1001

    def __init__(self: object, cliente: Cliente) -> None:
        self.__numero: int = Conta.codigo
        self.__cliente: Cliente = cliente
        self.__saldo: float = 0.0
        self.__limite: float = 100.0  # O cliente abre a conta com limite de R$ 100,00 atribuído automaticamente.
        self.__saldo_total: float = self._calcula_saldo_total  # É a soma do saldo em conta com o limite.
        Conta.codigo += 1

    def __str__(self: object) -> str:
        return f'Número da conta: {self.numero} \nCliente: {self.cliente.nome} ' \
               f'\nSaldo Total: {formata_float_str_moeda(self.saldo_total)}' \
               f'\nData de abertura da conta: {self.cliente.data_cadastro}'

    @property
    def numero(self: object) -> int:
        return self.__numero

    @property
    def cliente(self: object) -> Cliente:
        return self.__cliente

    @property  # para retornar um valor (getter)
    def saldo(self: object) -> float:
        return self.__saldo

    @saldo.setter  # para poder pegar e alterar o valor do saldo do usuário (setar).
    def saldo(self: object, valor: float) -> None:  # O valor do setter é sempre None.
        self.__saldo = valor

    @property  # para retornar um valor (getter)
    def limite(self: object) -> float:
        return self.__limite

    @limite.setter  # para poder pegar e alterar o valor do limite do usuário (setar).
    def limite(self: object, valor: float) -> None:  # O valor do setter é sempre None.
        self.__limite = valor

    @property
    def saldo_total(self: object) -> float:
        return self.__saldo_total

    @saldo_total.setter
    def saldo_total(self: object, valor: float) -> None:
        self.__saldo_total = valor

    @property
    def _calcula_saldo_total(self: object) -> float:
        return self.saldo + self.limite

    def depositar(self: object, valor: float) -> None:
        if valor > 0:
            self.saldo = self.saldo + valor  # 'self.saldo' é tipo getter, que retorna o valor.
            self.saldo_total = self._calcula_saldo_total
            print('Depósito efetuado com sucesso!')
        else:
            print('Erro ao efetuar depósito. Tente novamente!')

    def sacar(self: object, valor: float) -> None:
        if 0 < valor <= self.saldo_total:  # é a mesma coisa que: 'if valor > 0 and self.saldo_total >= valor':
            if self.saldo >= valor:  # se o saldo for maior que o valor do saque será efetuado o bloco do if a seguir.
                self.saldo = self.saldo - valor
                self.saldo_total = self._calcula_saldo_total
            else:  # não tendo o saldo suficiente para efetuar o saque é utilizado o valor do limite no bloco abaixo.
                restante: float = self.saldo - valor
                self.limite = self.limite + restante
                self.saldo = 0
                self.saldo_total = self._calcula_saldo_total
            print('Saque efetuado com sucesso!')

        else:
            print('Saque não realizado. Saldo insuficiente!')

    def transferir(self: object, destino: object, valor: float) -> None:
        if 0 < valor <= self.saldo_total:  # é a mesma coisa que: 'if valor > 0 and self.saldo_total >= valor':
            if self.saldo >= valor:  # se o saldo for maior que o valor do saque será efetuado o bloco do if a seguir.
                self.saldo = self.saldo - valor
                self.saldo_total = self._calcula_saldo_total
                destino.saldo = destino.saldo + valor
                destino.saldo_total = destino._calcula_saldo_total
                confirmar: str = input(f'Confirma transferência destino? s/n: ')
            else:
                restante: float = self.saldo - valor
                self.limite = self.limite + restante
                self.saldo = 0
                self.saldo_total = self._calcula_saldo_total
                destino.saldo = destino.saldo + valor
                destino.saldo_total = destino._calcula_saldo_total
            print('Transferência efetuado com sucesso!')
        else:
            print('Não foi possível efetuar a transferência. Saldo insuficiente!')
