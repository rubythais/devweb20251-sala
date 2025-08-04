#!/bin/bash

# Script de conveniência para gerenciar diferentes ambientes

case $1 in
    "dev"|"development")
        echo "🔧 Usando configurações de DESENVOLVIMENTO"
        export DJANGO_SETTINGS_MODULE=projadocato.settings.development
        shift
        python manage.py "$@"
        ;;
    "prod"|"production")
        echo "🚀 Usando configurações de PRODUÇÃO"
        export DJANGO_SETTINGS_MODULE=projadocato.settings.production
        shift
        python manage.py "$@"
        ;;
    "check-dev")
        echo "🔍 Verificando configurações de desenvolvimento..."
        python manage.py check --settings=projadocato.settings.development
        ;;
    "check-prod")
        echo "🔍 Verificando configurações de produção..."
        python manage.py check --settings=projadocato.settings.production
        ;;
    "collectstatic-dev")
        echo "📦 Coletando arquivos estáticos para desenvolvimento..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.development
        python manage.py collectstatic --noinput --clear
        ;;
    "collectstatic-prod")
        echo "📦 Coletando arquivos estáticos para produção..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.production
        python manage.py collectstatic --noinput --clear
        ;;
    "runserver-dev")
        echo "🔧 Iniciando servidor de desenvolvimento..."
        python manage.py runserver --settings=projadocato.settings.development
        ;;
    "gunicorn-dev")
        echo "🔧 Iniciando servidor de desenvolvimento com Gunicorn..."
        echo "📦 Coletando arquivos estáticos..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.development
        python manage.py collectstatic --noinput --clear
        echo "🚀 Iniciando Gunicorn..."
        gunicorn projadocato.wsgi:application --bind 0.0.0.0:8000 --reload --access-logfile - --error-logfile -
        ;;
    "gunicorn-dev-fast")
        echo "🔧 Iniciando servidor de desenvolvimento com Gunicorn (modo rápido)..."
        echo "📦 Coletando arquivos estáticos (se necessário)..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.development
        python manage.py collectstatic --noinput
        echo "🚀 Iniciando Gunicorn..."
        gunicorn projadocato.wsgi:application --bind 0.0.0.0:8000 --reload --access-logfile - --error-logfile -
        ;;
    "uvicorn-dev")
        echo "🔧 Iniciando servidor de desenvolvimento com Uvicorn (ASGI)..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.development
        uvicorn projadocato.asgi:application --host 0.0.0.0 --port 8000 --reload
        ;;
    "runserver-prod")
        echo "🚀 Iniciando servidor em modo produção..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.production
        gunicorn projadocato.wsgi:application --bind 0.0.0.0:8000
        ;;
    "gunicorn-prod")
        echo "🚀 Iniciando servidor de produção com Gunicorn..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.production
        gunicorn projadocato.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile -
        ;;
    "uvicorn-prod")
        echo "🚀 Iniciando servidor de produção com Uvicorn (ASGI)..."
        export DJANGO_SETTINGS_MODULE=projadocato.settings.production
        uvicorn projadocato.asgi:application --host 0.0.0.0 --port 8000 --workers 3
        ;;
    *)
        echo "📖 Uso do script:"
        echo "  ./run.sh dev [comando]     - Executa comando com settings de desenvolvimento"
        echo "  ./run.sh prod [comando]    - Executa comando com settings de produção"
        echo ""
        echo "🔍 Verificações:"
        echo "  ./run.sh check-dev         - Verifica configurações de desenvolvimento"
        echo "  ./run.sh check-prod        - Verifica configurações de produção"
        echo ""
        echo "📦 Arquivos estáticos:"
        echo "  ./run.sh collectstatic-dev - Coleta arquivos estáticos (desenvolvimento)"
        echo "  ./run.sh collectstatic-prod - Coleta arquivos estáticos (produção)"
        echo ""
        echo "🖥️  Servidores:"
        echo "  ./run.sh runserver-dev     - Servidor Django de desenvolvimento"
        echo "  ./run.sh gunicorn-dev      - Servidor Gunicorn de desenvolvimento (coleta static)"
        echo "  ./run.sh gunicorn-dev-fast - Servidor Gunicorn de desenvolvimento (rápido)"
        echo "  ./run.sh uvicorn-dev       - Servidor Uvicorn de desenvolvimento (ASGI)"
        echo "  ./run.sh runserver-prod    - Servidor Gunicorn de produção"
        echo "  ./run.sh gunicorn-prod     - Servidor Gunicorn de produção (configurado)"
        echo "  ./run.sh uvicorn-prod      - Servidor Uvicorn de produção (ASGI)"
        echo ""
        echo "📝 Exemplos:"
        echo "  ./run.sh dev migrate       - Roda migrations em desenvolvimento"
        echo "  ./run.sh prod collectstatic - Coleta arquivos estáticos para produção"
        echo "  ./run.sh dev makemigrations - Cria novas migrations"
        echo "  ./run.sh gunicorn-dev      - Servidor de desenvolvimento com Gunicorn"
        echo "  ./run.sh uvicorn-dev       - Servidor de desenvolvimento com Uvicorn"
        ;;
esac
