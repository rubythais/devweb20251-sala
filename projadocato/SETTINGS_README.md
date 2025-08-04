# Configuração de Settings para Desenvolvimento e Produção

## Estrutura

O projeto agora possui uma estrutura de settings organizada em múltiplos arquivos:

```
projadocato/settings/
├── __init__.py
├── base.py          # Configurações comuns a todos os ambientes
├── development.py   # Configurações específicas de desenvolvimento
└── production.py    # Configurações específicas de produção
```

## Como usar

### Desenvolvimento (padrão)

Por padrão, o `manage.py` está configurado para usar as configurações de desenvolvimento:

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
```

### Produção

Para usar as configurações de produção, você precisa definir a variável de ambiente `DJANGO_SETTINGS_MODULE`:

```bash
# Linux/Mac
export DJANGO_SETTINGS_MODULE=projadocato.settings.production

# Windows
set DJANGO_SETTINGS_MODULE=projadocato.settings.production

# Ou diretamente no comando
python manage.py runserver --settings=projadocato.settings.production
```

### Usando arquivo .env

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure as variáveis de ambiente no arquivo `.env`

3. Instale a biblioteca `python-decouple` para carregar variáveis do .env:
   ```bash
   pip install python-decouple
   ```

## Principais diferenças entre os ambientes

### Desenvolvimento
- `DEBUG = True`
- Banco de dados SQLite
- Django Debug Toolbar habilitado
- Email enviado para console
- Cache em memória local
- Logging no console

### Produção
- `DEBUG = False`
- Banco de dados PostgreSQL (configurável)
- Configurações de segurança habilitadas (HTTPS, HSTS, etc.)
- Email via SMTP
- Cache Redis (configurável)
- Logging em arquivo
- Variáveis de ambiente obrigatórias

## Variáveis de ambiente importantes

Para produção, configure estas variáveis:

- `SECRET_KEY`: Chave secreta do Django
- `DEBUG`: False para produção
- `ALLOWED_HOSTS`: Domínios permitidos (separados por vírgula)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Configuração do banco
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, etc.: Configuração de email
- `REDIS_URL`: URL do Redis para cache
- `CSRF_TRUSTED_ORIGINS`: Origens confiáveis para CSRF

## Comandos úteis

```bash
# Rodar com settings específicos
python manage.py runserver --settings=projadocato.settings.development
python manage.py runserver --settings=projadocato.settings.production

# Verificar configurações
python manage.py check --settings=projadocato.settings.production

# Coletar arquivos estáticos (produção)
python manage.py collectstatic --settings=projadocato.settings.production
```
