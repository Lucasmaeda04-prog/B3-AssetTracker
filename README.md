# B3 Monitor - Sistema de Monitoramento de Ativos

Este projeto é um sistema de monitoramento de ativos da B3 que permite acompanhar preços e receber alertas por email quando os valores atingem determinados limites.

## Pré-requisitos

- Docker
- Docker Compose
- Git
- Conta Gmail para envio de emails

## Configuração do Ambiente

1. Clone o repositório
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Configure o arquivo de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```plaintext
# Database
POSTGRES_DB=b3monitor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Configurando o Email do Gmail

Para usar o Gmail para envio de emails, siga estes passos:

1. Acesse sua conta do Gmail
2. Vá em Gerenciar sua Conta Google
3. Na seção "Segurança":
   - Ative a "Verificação em duas etapas"
   - Depois de ativada, vá em "Senhas de app"
   - Selecione "App: Outro (nome personalizado)"
   - Digite um nome (ex: "B3Monitor")
   - Clique em "Gerar"
4. Copie a senha gerada (16 caracteres) e cole no arquivo `.env` no campo `EMAIL_HOST_PASSWORD`
5. Coloque seu email Gmail no campo `EMAIL_HOST_USER`

## Instalação e Execução

1. Construa e inicie os containers
```bash
docker compose up --build
```

O sistema estará disponível em `http://localhost:8000`

## Configuração Inicial

### 1. Criar um Superusuário

Em um novo terminal, com os containers rodando, execute:

```bash
# Acesse o container da aplicação
docker compose exec web bash

# Crie um superusuário
python manage.py createsuperuser
```

Siga as instruções para criar seu usuário administrativo:
- Digite seu email
- Digite sua senha
- Confirme sua senha

### 2. Acessar o Sistema

1. Acesse `http://localhost:8000/admin`
2. Faça login com as credenciais do superusuário criado

### 3. Cadastrar um Ativo

1. No painel administrativo, clique em "Ativos"
2. Clique no botão "ADICIONAR ATIVO"
3. Preencha os campos:
   - **Sigla**: Código do ativo na B3 (ex: PETR4)
   - **Nome**: Nome descritivo do ativo
   - **Email para Alertas**: Email que receberá as notificações
   - **Limite Superior**: Preço máximo para alertas
   - **Limite Inferior**: Preço mínimo para alertas
   - **Intervalo de Checagem**: Frequência de verificação em minutos

4. Clique em "SALVAR"

## Monitoramento

- O sistema verificará automaticamente os preços dos ativos nos intervalos configurados
- Alertas serão enviados por email quando o preço ultrapassar os limites estabelecidos
- Você pode visualizar o histórico de preços acessando cada ativo na interface administrativa

## Visualização dos Dados

1. Acesse `http://localhost:8000`
2. Clique em um ativo para ver:
   - Gráfico de variação de preço
   - Limites configurados
   - Histórico de preços

## Problemas Comuns

### O sistema não consegue verificar o ativo

- Verifique se a sigla está correta (ex: PETR4, não PETR4.SA)
- Confirme se o ativo está disponível para negociação
- Verifique os logs do Docker para mais detalhes:
```bash
docker compose logs celery | grep "ativo"
```

### Emails não estão sendo recebidos

- Verifique se configurou corretamente o arquivo `.env` com as credenciais do Gmail
- Confirme se a senha de app foi gerada corretamente
- Verifique se o email foi cadastrado corretamente no ativo
- Verifique os logs do sistema para erros de envio:
```bash
docker compose logs celery | grep "mail"
```

## Comandos Úteis

```bash
# Reiniciar os containers
docker-compose restart

# Ver logs
docker-compose logs -f

# Parar os containers
docker-compose down

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar novas migrações
docker-compose exec web python manage.py makemigrations
```