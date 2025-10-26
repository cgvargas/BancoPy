# Guia R�pido - BancoPy Django

## Iniciando o Projeto pela Primeira Vez

### 1. Criar Superusu�rio (Admin)

```bash
python manage.py createsuperuser
```

Voc� ser� solicitado a fornecer:
- Username (nome de usu�rio)
- Email (opcional)
- Password (senha - digite duas vezes)

Exemplo:
```
Username: admin
Email address: admin@bancoppy.com
Password: ********
Password (again): ********
Superuser created successfully.
```

### 2. Iniciar o Servidor

```bash
python manage.py runserver
```

O servidor iniciar� em: http://127.0.0.1:8000

### 3. Acessar o Sistema

**Interface Web Principal:**
- URL: http://localhost:8000
- N�o requer login
- Acesso a todas as funcionalidades do banco

**Django Admin:**
- URL: http://localhost:8000/admin
- Requer login com as credenciais do superusu�rio
- Interface administrativa completa

## Primeiros Passos

### 1. Criar sua primeira conta

1. Acesse http://localhost:8000
2. Clique em "Abrir Conta"
3. Preencha os dados:
   - Nome: Jo�o Silva
   - Email: joao@email.com
   - CPF: 123.456.789-00
   - Data de Nascimento: Selecione uma data
4. Clique em "Criar Conta"

A conta ser� criada automaticamente com:
- Saldo: R$ 0,00
- Limite: R$ 100,00
- Saldo Total: R$ 100,00

### 2. Fazer um dep�sito

1. Na p�gina da conta, clique em "Dep�sito"
2. Digite o valor (ex: 500,00 ou 500.00)
3. Clique em "Confirmar Dep�sito"

### 3. Criar mais contas para testar transfer�ncias

Repita o processo de cria��o de conta para ter pelo menos 2 contas.

### 4. Fazer uma transfer�ncia

1. Na p�gina de uma conta, clique em "Transferir"
2. Digite o n�mero da conta destino
3. Digite o valor da transfer�ncia
4. Clique em "Confirmar Transfer�ncia"

### 5. Visualizar hist�rico

Na p�gina de detalhes da conta, role at� "�ltimas Transa��es" para ver o hist�rico.

## Comandos �teis

### Parar o servidor
Pressione `Ctrl + C` no terminal

### Reiniciar o servidor
```bash
python manage.py runserver
```

### Executar em outra porta
```bash
python manage.py runserver 8080
```

### Limpar o banco de dados
```bash
# ATEN��O: Isso apagar� TODOS os dados!
del db.sqlite3  # Windows
python manage.py migrate
python manage.py createsuperuser  # Criar novo superusu�rio
```

### Ver estrutura do banco
```bash
python manage.py dbshell
.tables  # Lista todas as tabelas
.schema contas_conta  # Ver estrutura da tabela conta
.quit  # Sair
```

## Dicas

1. **Formato de Valores**: Use v�rgula ou ponto como separador decimal
   -  100,50
   -  100.50
   -  1000
   - L 100,50,00

2. **CPF**: Por enquanto aceita qualquer formato
   - Sugest�o: Use o formato 000.000.000-00

3. **Navega��o**: Use os bot�es "Voltar" para retornar �s p�ginas anteriores

4. **Admin**: Use o Django Admin para visualiza��es mais detalhadas e buscas avan�adas

## Testando o Sistema Completo

Execute este fluxo para testar todas as funcionalidades:

1.  Criar conta do Jo�o
2.  Criar conta da Maria
3.  Depositar R$ 1000,00 na conta do Jo�o
4.  Sacar R$ 200,00 da conta do Jo�o
5.  Transferir R$ 300,00 do Jo�o para Maria
6.  Verificar saldos finais
7.  Visualizar hist�rico de transa��es
8.  Acessar o admin e explorar os relat�rios

## Problemas Comuns

### "No such table: contas_conta"
Execute as migra��es:
```bash
python manage.py migrate
```

### "That port is already in use"
O servidor j� est� rodando em outra janela ou use outra porta:
```bash
python manage.py runserver 8080
```

### Esqueci a senha do admin
Crie um novo superusu�rio ou redefina a senha:
```bash
python manage.py createsuperuser
```

## Pr�ximos Passos

Depois de se familiarizar com o sistema, voc� pode:

1. Explorar o c�digo em `contas/models.py` para entender a l�gica
2. Customizar os templates em `contas/templates/`
3. Adicionar novas funcionalidades em `contas/views.py`
4. Modificar a apar�ncia editando os templates HTML
5. Estudar o Django Admin em `contas/admin.py`

Divirta-se explorando o BancoPy! <�
