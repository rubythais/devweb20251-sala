# Deploy do Adocato no Render.com

## 📋 Pré-requisitos

1. Conta no [Render.com](https://render.com)
2. Repositório Git (GitHub, GitLab, ou Bitbucket)
3. Código commitado no repositório

## 🚀 Passos para Deploy

### 1. Preparar o repositório

Certifique-se de que os seguintes arquivos estão no seu repositório:

- `build.sh` - Script de build (na raiz do repositório)
- `render.yaml` - Configuração do Render (na raiz do repositório)
- `projadocato/requirements_render.txt` - Dependências Python
- Configurações de produção em `projadocato/settings/production.py`

### 2. Criar o serviço no Render

#### Opção A: Deploy automático com render.yaml
1. Faça o commit do arquivo `render.yaml`
2. No Render Dashboard, clique em "New +"
3. Selecione "Blueprint"
4. Conecte seu repositório
5. O Render criará automaticamente os serviços

#### Opção B: Deploy manual
1. No Render Dashboard, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório
4. Configure as seguintes opções:

**Configurações básicas:**
- **Name**: `adocato`
- **Environment**: `Python`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn projadocato.wsgi:application`

**Configurações avançadas:**
- **Python Version**: `3.12.0`

### 3. Configurar variáveis de ambiente

No painel do Render, vá em "Environment" e adicione:

**Obrigatórias:**
```
DJANGO_SETTINGS_MODULE=projadocato.settings.production
SECRET_KEY=[será gerada automaticamente]
RENDER_EXTERNAL_HOSTNAME=[seu-app].onrender.com
```

**Opcionais:**
```
DEBUG=False
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
DEFAULT_FROM_EMAIL=noreply@adocato.com
SECURE_SSL_REDIRECT=True
```

### 4. Adicionar banco de dados PostgreSQL

1. No Render Dashboard, clique em "New +"
2. Selecione "PostgreSQL"
3. Configure:
   - **Name**: `adocato-db`
   - **Plan**: Free (para desenvolvimento)
4. Após criado, copie a `DATABASE_URL`
5. Volte ao seu Web Service e adicione a variável:
   ```
   DATABASE_URL=[cole a URL aqui]
   ```

### 5. Adicionar Redis (opcional)

1. No Render Dashboard, clique em "New +"
2. Selecione "Redis"
3. Configure:
   - **Name**: `adocato-redis`  
   - **Plan**: Free
4. Após criado, copie a `REDIS_URL`
5. Adicione no Web Service:
   ```
   REDIS_URL=[cole a URL aqui]
   ```

## 🔧 Comandos de gerenciamento

Para executar comandos Django no Render:

1. Vá ao seu Web Service no Dashboard
2. Clique na aba "Shell"
3. Execute comandos como:

```bash
# Migrations
python manage.py migrate --settings=projadocato.settings.production

# Criar superuser
python manage.py createsuperuser --settings=projadocato.settings.production

# Coletar arquivos estáticos
python manage.py collectstatic --noinput --settings=projadocato.settings.production

# Shell Django
python manage.py shell --settings=projadocato.settings.production
```

## 📁 Estrutura de arquivos importantes

```
/                               # Raiz do repositório
├── build.sh                    # Script de build do Render
├── render.yaml                 # Configuração automática do Render
└── projadocato/                # Diretório do projeto Django
    ├── requirements_render.txt # Dependências para produção
    ├── projadocato/
    │   ├── settings/
    │   │   ├── production.py   # Settings para produção
    │   │   └── ...
    │   ├── wsgi.py             # Configurado para produção
    │   └── ...
    └── ...
```

## 🔍 Monitoramento e logs

- **Logs**: Disponíveis na aba "Logs" do seu serviço
- **Métricas**: Aba "Metrics" mostra uso de CPU/memória
- **Saúde**: Render monitora automaticamente a saúde da aplicação

## 🛠️ Troubleshooting

### Erro de build
- Verifique se `build.sh` tem permissões de execução
- Confirme que `requirements_render.txt` tem todas as dependências

### Erro de static files
- Certifique-se que `collectstatic` rodou no build
- Verifique se `STATIC_ROOT` está configurado

### Erro de database
- Confirme que `DATABASE_URL` está configurada
- Verifique se as migrations foram executadas

### Erro de SECRET_KEY
- Gere uma nova SECRET_KEY nas variáveis de ambiente
- Use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

## 📝 Notas importantes

1. **Plan Free**: Tem limitações de recursos e pode "dormir" após inatividade
2. **HTTPS**: Render fornece HTTPS automaticamente
3. **Custom Domain**: Disponível em plans pagos
4. **Backups**: Configure backups regulares do PostgreSQL
5. **Monitoring**: Use ferramentas como Sentry para monitoramento de erros

## 🔄 Atualizações

Para atualizar a aplicação:
1. Faça commit das mudanças no repositório
2. O Render irá automaticamente fazer o redeploy
3. Monitore os logs durante o processo
