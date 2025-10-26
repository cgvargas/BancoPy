# Guia Rápido - BancoPy Django

## Iniciando o Projeto pela Primeira Vez

### 1. Criar Superusuário (Admin)

```bash
python manage.py createsuperuser
```

Você será solicitado a fornecer:
- Username (nome de usuário)
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

O servidor iniciará em: http://127.0.0.1:8000

### 3. Acessar o Sistema

**Interface Web Principal:**
- URL: http://localhost:8000
- Não requer login
- Acesso a todas as funcionalidades do banco

**Django Admin:**
- URL: http://localhost:8000/admin
- Requer login com as credenciais do superusuário
- Interface administrativa completa

## Primeiros Passos

### 1. Criar sua primeira conta

1. Acesse http://localhost:8000
2. Clique em "Abrir Conta"
3. Preencha os dados:
   - Nome: João Silva
   - Email: joao@email.com
   - CPF: 123.456.789-00
   - Data de Nascimento: Selecione uma data
4. Clique em "Criar Conta"

A conta será criada automaticamente com:
- Saldo: R$ 0,00
- Limite: R$ 100,00
- Saldo Total: R$ 100,00

### 2. Fazer um depósito

1. Na página da conta, clique em "Depósito"
2. Digite o valor (ex: 500,00 ou 500.00)
3. Clique em "Confirmar Depósito"

### 3. Criar mais contas para testar transferências

Repita o processo de criação de conta para ter pelo menos 2 contas.

### 4. Fazer uma transferência

1. Na página de uma conta, clique em "Transferir"
2. Digite o número da conta destino
3. Digite o valor da transferência
4. Clique em "Confirmar Transferência"

### 5. Visualizar histórico

Na página de detalhes da conta, role até "Últimas Transações" para ver o histórico.

## Comandos Úteis

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
# ATENÇÃO: Isso apagará TODOS os dados!
del db.sqlite3  # Windows
python manage.py migrate
python manage.py createsuperuser  # Criar novo superusuário
```

### Ver estrutura do banco
```bash
python manage.py dbshell
.tables  # Lista todas as tabelas
.schema contas_conta  # Ver estrutura da tabela conta
.quit  # Sair
```

## Dicas

1. **Formato de Valores**: Use vírgula ou ponto como separador decimal
   -  100,50
   -  100.50
   -  1000
   - L 100,50,00

2. **CPF**: Por enquanto aceita qualquer formato
   - Sugestão: Use o formato 000.000.000-00

3. **Navegação**: Use os botões "Voltar" para retornar às páginas anteriores

4. **Admin**: Use o Django Admin para visualizações mais detalhadas e buscas avançadas

## Testando o Sistema Completo

Execute este fluxo para testar todas as funcionalidades:

1.  Criar conta do João
2.  Criar conta da Maria
3.  Depositar R$ 1000,00 na conta do João
4.  Sacar R$ 200,00 da conta do João
5.  Transferir R$ 300,00 do João para Maria
6.  Verificar saldos finais
7.  Visualizar histórico de transações
8.  Acessar o admin e explorar os relatórios

## Problemas Comuns

### "No such table: contas_conta"
Execute as migrações:
```bash
python manage.py migrate
```

### "That port is already in use"
O servidor já está rodando em outra janela ou use outra porta:
```bash
python manage.py runserver 8080
```

### Esqueci a senha do admin
Crie um novo superusuário ou redefina a senha:
```bash
python manage.py createsuperuser
```

## Próximos Passos

Depois de se familiarizar com o sistema, você pode:

1. Explorar o código em `contas/models.py` para entender a lógica
2. Customizar os templates em `contas/templates/`
3. Adicionar novas funcionalidades em `contas/views.py`
4. Modificar a aparência editando os templates HTML
5. Estudar o Django Admin em `contas/admin.py`

Divirta-se explorando o BancoPy! <æ
