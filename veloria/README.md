# Veloria Grand Hotel — Secure Booking System

> Elegant. Secure. Unforgettable.

A secure hotel booking web application built with Django as part of the IKB21503 Secure Software Development course at Universiti Kuala Lumpur.

---

## Security Features

- OWASP Top 10 compliant
- Argon2 password hashing
- CSRF protection on all forms
- Role-Based Access Control (Admin / Guest)
- Session timeout (30 minutes)
- Input validation (whitelist + regex)
- File upload security (MIME check, UUID rename)
- Audit logging for all security events
- Custom error pages (400, 403, 404, 500)
- XSS prevention via Django auto-escaping
- IDOR prevention on all endpoints
- Account lockout after 5 failed login attempts

---

## Tech Stack

- **Framework:** Django 4.2.13
- **Language:** Python 3.10+
- **Database:** SQLite (development)
- **Frontend:** Bootstrap 5, Font Awesome
- **Password Hashing:** Argon2

---

## Installation & Setup

Requires **Python 3.10 or newer** and Git.

### Quick setup (recommended)

```bash
git clone https://github.com/AdliFirdaus/veloria_grand_hotel.git
cd veloria_grand_hotel/veloria
```

Then run the setup script. It creates the virtual environment, installs dependencies, creates `.env` with a freshly generated `SECRET_KEY`, and sets up the database (including the default room types).

```bash
setup.bat          # Windows
./setup.sh         # Linux/Mac
```

Create an admin account and start the server:

```bash
venv\Scripts\python manage.py createsuperuser     # Windows
venv\Scripts\python manage.py runserver

venv/bin/python manage.py createsuperuser         # Linux/Mac
venv/bin/python manage.py runserver
```

Visit: http://127.0.0.1:8000

### Manual setup

```bash
cd veloria_grand_hotel/veloria
python -m venv venv
venv\Scripts\activate                  # Windows
source venv/bin/activate               # Linux/Mac
pip install -r requirements.txt
cp .env.example .env                   # Windows: copy .env.example .env
```

Edit `.env` and replace `SECRET_KEY` with a random value. You can generate one with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then:

```bash
python manage.py migrate               # also creates the default room types
python manage.py createsuperuser
python manage.py runserver
```

### Notes

- `.env`, `db.sqlite3`, `media/` and `logs/` are not in the repository. Each person gets their own local database and uploads.
- `DEBUG=True` in `.env.example` is for local development only. Set `DEBUG=False` and the `SECURE_*` / `*_COOKIE_SECURE` options to `True` when deploying behind HTTPS.

---

## Project Structure

```
veloria/
├── config/          # Django settings, urls, wsgi
├── accounts/        # User auth, RBAC, profiles
├── rooms/           # Room management CRUD
├── bookings/        # Booking system CRUD
├── audit/           # Audit logging
├── hotel/           # Home, dashboard, error pages
├── templates/       # All HTML templates
├── static/          # CSS, JS, images
├── .env.example     # Environment template
├── requirements.txt # Dependencies
└── manage.py
```

---

## Default Roles

| Role  | Access |
|-------|--------|
| Admin | Full access — rooms, bookings, audit logs |
| Guest | Browse rooms, manage own bookings, edit profile |

---

## Team Members

| Member | Role |
|--------|------|
| Member 1 | Backend & Security Controls |
| Member 2 | Frontend & System Features |
| Member 3 | Security Design & Vulnerability Analysis |
| Member 4 | Validation, Evidence & GitHub |

---

## Course Information

- **Course:** IKB21503 Secure Software Development
- **Institution:** Universiti Kuala Lumpur (UniKL MIIT)
- **Semester:** 2025/October
