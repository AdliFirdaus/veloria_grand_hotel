@echo off
REM Veloria Grand Hotel - one-time setup for Windows
cd /d "%~dp0"

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv || goto :error
)

echo Installing dependencies...
venv\Scripts\python -m pip install --upgrade pip >nul
venv\Scripts\python -m pip install -r requirements.txt || goto :error

if not exist .env (
    echo Creating .env from .env.example with a new SECRET_KEY...
    venv\Scripts\python -c "from django.core.management.utils import get_random_secret_key as g; import re; t=open('.env.example').read(); open('.env','w').write(re.sub(r'(?m)^SECRET_KEY=.*$', lambda m: 'SECRET_KEY='+g(), t))" || goto :error
)

echo Running database migrations...
venv\Scripts\python manage.py migrate || goto :error

echo.
echo Setup complete.
echo   Create an admin account : venv\Scripts\python manage.py createsuperuser
echo   Start the server        : venv\Scripts\python manage.py runserver
echo   Then open               : http://127.0.0.1:8000
goto :eof

:error
echo.
echo Setup failed. See the error above.
exit /b 1
