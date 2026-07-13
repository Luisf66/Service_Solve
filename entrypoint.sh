#!/bin/sh

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Rodando migrations..."
python manage.py migrate --noinput

echo "Iniciando servidor..."
gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2