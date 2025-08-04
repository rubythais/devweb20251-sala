# Guia de Servidores - Django Adocato

## 🖥️ Opções de Servidor

O projeto oferece múltiplas opções para executar o servidor, cada uma adequada para diferentes cenários:

### 📋 Resumo dos Comandos

| Comando | Servidor | Ambiente | Protocolo | Uso |
|---------|----------|----------|-----------|-----|
| `./run.sh runserver-dev` | Django Dev | Desenvolvimento | HTTP | Debug e desenvolvimento |
| `./run.sh gunicorn-dev` | Gunicorn | Desenvolvimento | HTTP (WSGI) | Teste local com servidor de produção |
| `./run.sh gunicorn-dev-fast` | Gunicorn | Desenvolvimento | HTTP (WSGI) | Desenvolvimento iterativo (rápido) |
| `./run.sh uvicorn-dev` | Uvicorn | Desenvolvimento | HTTP (ASGI) | Apps com WebSockets/async |
| `./run.sh runserver-prod` | Gunicorn | Produção | HTTP (WSGI) | Deploy simples |
| `./run.sh gunicorn-prod` | Gunicorn | Produção | HTTP (WSGI) | Produção com workers |
| `./run.sh uvicorn-prod` | Uvicorn | Produção | HTTP (ASGI) | Produção async |

## 🔧 Desenvolvimento

### Django Development Server
```bash
./run.sh runserver-dev
```
- **Quando usar**: Desenvolvimento diário, debug
- **Características**: 
  - Auto-reload em mudanças de código
  - Debug toolbar ativo
  - Mensagens de erro detalhadas
  - Não adequado para produção

### Gunicorn Development  
```bash
./run.sh gunicorn-dev
```
- **Quando usar**: Testar comportamento próximo à produção localmente
- **Características**:
  - Servidor WSGI como produção
  - Auto-reload ativo (`--reload`)
  - **Coleta arquivos estáticos automaticamente** (--clear)
  - WhiteNoise middleware para servir static files
  - Logs visíveis no terminal
  - 1 worker (adequado para desenvolvimento)

### Gunicorn Development (Rápido)
```bash
./run.sh gunicorn-dev-fast
```
- **Quando usar**: Desenvolvimento contínuo com Gunicorn
- **Características**:
  - Mesmo que gunicorn-dev, mas sem `--clear`
  - Coleta apenas arquivos novos/modificados
  - Inicialização mais rápida
  - Ideal para desenvolvimento iterativo

### Uvicorn Development
```bash
./run.sh uvicorn-dev
```
- **Quando usar**: Desenvolvimento de features assíncronas
- **Características**:
  - Servidor ASGI para aplicações async
  - Auto-reload ativo
  - Suporte a WebSockets
  - Ideal para testes de performance

## 🚀 Produção

### Gunicorn Production (Simples)
```bash
./run.sh runserver-prod
```
- **Quando usar**: Deploy básico, containers simples
- **Características**:
  - Configuração mínima
  - 1 worker
  - Bind em todas as interfaces (0.0.0.0:8000)

### Gunicorn Production (Configurado)
```bash
./run.sh gunicorn-prod
```
- **Quando usar**: Produção com alta disponibilidade
- **Características**:
  - 3 workers (ajustável)
  - Logs estruturados
  - Configuração otimizada
  - **Recomendado para Render.com**

### Uvicorn Production
```bash
./run.sh uvicorn-prod
```
- **Quando usar**: Apps com requisitos assíncronos em produção
- **Características**:
  - Múltiplos workers
  - Performance para I/O assíncrono
  - Suporte a WebSockets

## 📁 Arquivos Estáticos

### 🔍 **Problema**: Gunicorn não serve arquivos estáticos

Diferente do Django dev server, o Gunicorn não serve arquivos estáticos automaticamente. A solução implementada:

1. **WhiteNoise middleware** - Configurado em `development.py`
2. **Coleta automática** - Executada antes de iniciar o Gunicorn
3. **Comandos específicos** - Para gerenciar static files

### 📦 **Comandos de Static Files**:

```bash
# Coleta arquivos estáticos para desenvolvimento
./run.sh collectstatic-dev

# Coleta arquivos estáticos para produção  
./run.sh collectstatic-prod

# Servidores que coletam automaticamente
./run.sh gunicorn-dev      # Coleta com --clear (limpa antes)
./run.sh gunicorn-dev-fast # Coleta apenas novos/modificados
```

### ⚙️ **Como funciona**:

1. **Middleware WhiteNoise**: Adicionado ao `MIDDLEWARE` em desenvolvimento
2. **STATICFILES_STORAGE**: Configurado para compressão
3. **Pasta staticfiles**: Criada automaticamente se não existir
4. **Coleta automática**: Executada pelos comandos gunicorn-dev

### 🎯 **Fluxo recomendado**:

```bash
# Primeira vez ou após mudanças nos static files
./run.sh gunicorn-dev

# Desenvolvimento contínuo (mais rápido)
./run.sh gunicorn-dev-fast

# Se houver problemas com static files
./run.sh collectstatic-dev
```

## ⚙️ Configurações Específicas

### Gunicorn Development
```bash
gunicorn projadocato.wsgi:application \
  --bind 0.0.0.0:8000 \
  --reload \
  --access-logfile - \
  --error-logfile -
```

### Gunicorn Production
```bash
gunicorn projadocato.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --access-logfile - \
  --error-logfile -
```

### Uvicorn Development
```bash
uvicorn projadocato.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

### Uvicorn Production
```bash
uvicorn projadocato.asgi:application \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 3
```

## 🎯 Recomendações de Uso

### Para Desenvolvimento Local:
1. **Início rápido**: `./run.sh runserver-dev`
2. **Teste de produção**: `./run.sh gunicorn-dev`
3. **Desenvolvimento contínuo**: `./run.sh gunicorn-dev-fast`
4. **Features async**: `./run.sh uvicorn-dev`

### Para Deploy/Produção:
1. **Render.com**: `./run.sh gunicorn-prod` (configurado no build.sh)
2. **Docker**: `./run.sh gunicorn-prod`
3. **Apps async**: `./run.sh uvicorn-prod`

### Para Debug de Performance:
- Use `gunicorn-dev` para simular comportamento de produção
- Use `uvicorn-dev` para testar performance assíncrona
- Compare diferentes servidores em ambiente local

## 🔍 Monitoramento

Todos os comandos de produção incluem logs estruturados:
- **Access logs**: Requisições HTTP
- **Error logs**: Erros do servidor
- **Django logs**: Logs da aplicação (via settings)

## 📝 Notas Importantes

1. **Porta padrão**: Todos os servidores usam porta 8000
2. **Host binding**: 0.0.0.0 permite acesso externo
3. **Workers**: Produção usa 3 workers (ajustável conforme CPU)
4. **Auto-reload**: Apenas em desenvolvimento
5. **Debug**: Controlado via DJANGO_SETTINGS_MODULE
