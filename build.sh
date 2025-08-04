#!/usr/bin/env bash
# exit on error
set -o errexit

# Change to project directory
cd projadocato

# Install dependencies
pip install -r requirements_render.txt

# Collect static files
python manage.py collectstatic --noinput --settings=projadocato.settings.production

# Run migrations
python manage.py migrate --settings=projadocato.settings.production

#Cria um superusuário com a senha definida no ambiente
python manage.py runscript createsuperuser --settings=projadocato.settings.production
