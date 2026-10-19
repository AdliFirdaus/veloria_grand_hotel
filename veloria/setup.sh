#!/usr/bin/env bash
# Veloria Grand Hotel - one-time setup for Linux/macOS
set -e
cd "$(dirname "$0")"

if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Installing dependencies..."
venv/bin/python -m pip install --upgrade pip > /dev/null
venv/bin/python -m pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "Creating .env from .env.example with a new SECRET_KEY..."
    venv/bin/python -c "from django.core.management.utils import get_random_secret_key as g; import re; t=open('.env.example').read(); open('.env','w').write(re.sub(r'(?m)^SECRET_KEY=.*$', lambda m: 'SECRET_KEY='+g(), t))"
fi

echo "Running database migrations..."
venv/bin/python manage.py migrate

echo
echo "Setup complete."
echo "  Create an admin account : venv/bin/python manage.py createsuperuser"
echo "  Start the server        : venv/bin/python manage.py runserver"
echo "  Then open               : http://127.0.0.1:8000"
