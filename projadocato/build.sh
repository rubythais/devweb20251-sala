#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements_render.txt

# Collect static files
python manage.py collectstatic --noinput --settings=projadocato.settings.production

# Run migrations
python manage.py migrate --settings=projadocato.settings.production
