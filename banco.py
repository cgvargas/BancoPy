import datetime
from typing import List
from time import sleep

from models.cliente import Cliente
from models.conta import Conta

contas: List[Conta] = []


def main() -> None:
    menu()


def menu() -> None:
    print(' ')
    print(' ')
    print('    ========        ====      ======      ===   ===    ===  ')
    print('    ===    ===     ==  ==     === ===     ===   ===   ===   ')
    print('    ===    ===   ===    ===   ===  ===    ===   ===  ===    ')
    print('    =========   ============  ===   ===   ===   ======      ')
    print('    =========   ============  ===    ===  ===   ======      ')
    print('    ===    ===  ===      ===  ===     === ===   ===  ===    ')
    print('    ===    ===  ===      ===  ===      ======   ===   ===   ')
    print('    ========    ===      ===  ===       =====   ===    ===  ')
    print(' ')
    print(' ')

    print('Selecione Serviço:\n')
    print('1 - Abertura de contas')
    print('2 - Efetuar saque')
    print('3 - Efetuar depósito')
    print('4 - Efetuar transferência')
    print('5 - Flog de contas')
    print('6 - Sair do sistema\n')

    opcao: int = int(input('>>> '))

    if opcao == 1:
        criar_conta()
    elif opcao == 2:
        efetuar_saque()
    elif opcao == 3:
        efetuar_deposito()
    elif opcao == 4:
        efetuar_transferencia()
    elif opcao == 5:
        listar_contas()
    elif opcao == 6:
        print('Volte Sempre!')
        sleep(2)
        exit(0)
    else:
        print('Opção Inválida: ')
        menu()


def criar_conta() -> None:
    try:
        print('Informe os dados do cliente:\n ')
        nome: str = input('Nome do cliente: ')
        email: str = input('Email do cliente: ')
        cpf: str = input('CPF do cliente: ')
        data_nascimento: str = input('Data de nascimento do cliente: ')
        data_cadastro: datetime = datetime.datetime.today()

        cliente: Cliente = Cliente(nome, email, cpf, data_nascimento, data_cadastro)
        conta: Conta = Conta(cliente)
        contas.append(conta)
    except:
        print('Dados Incorretos!')
        sleep(2)
        menu()
    else:
        print('Conta criada com sucesso.\n')
        print('---------------')
        print('Dados da conta:')
        print('---------------')
        print(conta)
        sleep(2)
        menu()


def efetuar_saque() -> None:
    if len(contas) > 0:
        numero: int = int(input('Informe o número da sua conta: '))

        conta: Conta = buscar_conta_por_numero(numero)

        if conta:
            valor: float = float(input('Informe o valor do saque: '))
            conta.sacar(valor)
        else:
            print(f'Não foi encontrada a conta com número {numero}')
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def efetuar_deposito() -> None:
    if len(contas) > 0:
        try:
            numero: int = int(input('Informe o número da sua conta: '))
            conta: Conta = buscar_conta_por_numero(numero)

            if conta:
                valor_input: str = input('Informe o valor do depósito (ex: 100,50): ')
                # Substitui vírgula por ponto para conversão
                valor_input = valor_input.replace(',', '.')
                valor: float = float(valor_input)

                if valor <= 0:
                    print('O valor do depósito deve ser positivo.')
                else:
                    conta.depositar(valor)
            else:
                print(f'Não foi encontrada a conta com número {numero}')
        except ValueError:
            print('Erro: Valor inválido. Por favor, informe um número válido.')
        except Exception as e:
            print(f'Erro ao processar depósito: {str(e)}')
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def efetuar_transferencia() -> None:
    if len(contas) > 0:
        numero_o: int = int(input('Informe o número da sua conta: '))
        conta_o: Conta = buscar_conta_por_numero(numero_o)
        if conta_o:  # conta de onde o dinheiro vai sair
            numero_d: int = int(input('Informe o numero da conta destino: '))
            conta_d: Conta = buscar_conta_por_numero(numero_d)
            if conta_d:  # conta para onde o dinheiro vai entrar.
                valor: float = float(input('Informe o valor da transferência: '))
                conta_o.transferir(conta_d, valor)
            else:
                print(f'A conta destino com número {numero_d} não foi encontrada!')
        else:
            print(f'A sua conta com número {numero_o} não foi encontrada!')
    else:
        print('Ainda não existem contas cadastradas.')
    sleep(2)
    menu()


def listar_contas() -> None:
    if len(contas) > 0:
        print('Listagem de contas:\n ')
        for conta in contas:  # 'contas' está definida como lista vazia no início do programa.
            print(conta)  # vai imprimir o 'str' de contas
            print('---------------------------------------')
            sleep(1)
    else:
        print('Não existem contas cadastradas. ')
    sleep(2)
    menu()


def buscar_conta_por_numero(numero: int) -> Conta:
    c: Conta = None
    if len(contas) > 0:
        for conta in contas:
            if conta.numero == numero:
                c = conta
    return c


if __name__ == '__main__':
    main()
