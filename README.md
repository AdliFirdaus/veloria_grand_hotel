# Veloria Grand Hotel — Secure Booking System

> Elegant. Secure. Unforgettable.

A secure hotel booking web application built with Django for the **IKB21503 Secure Software Development** course at Universiti Kuala Lumpur (UniKL MIIT).

Guests can browse rooms, make and cancel bookings, and manage their profile. Admins manage rooms, approve or update bookings, and review the security audit log.

---

## Contents

- [Quick Start](#quick-start)
- [Creating an Admin Account](#creating-an-admin-account)
- [Using the App](#using-the-app)
- [Manual Setup](#manual-setup)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Security Features](#security-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Team & Course](#team-members)

---

## Quick Start

**You need:** [Python 3.10 or newer](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads).

**1. Clone the repository**

```bash
git clone https://github.com/AdliFirdaus/veloria_grand_hotel.git
cd veloria_grand_hotel/veloria
```

**2. Run the setup script**

| Windows | Linux / macOS |
|---------|---------------|
| `setup.bat` | `./setup.sh` |

The script runs once and does everything for you. It:

- creates a virtual environment (`venv/`)
- installs all dependencies from `requirements.txt`
- creates `.env` with a freshly generated `SECRET_KEY`
- creates the database and adds the default room types (Deluxe Room, Executive Suite, Presidential Suite)

**3. Start the server**

```bash
# Windows
venv\Scripts\python manage.py runserver

# Linux / macOS
venv/bin/python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser. To stop the server, press `Ctrl + C`.

---

## Creating an Admin Account

The app has its own role system (`guest` / `admin`) on top of Django's superuser flag. **`createsuperuser` creates a user with the `guest` role**, so you need to promote that user to `admin` before they can manage rooms, bookings and audit logs.

**1. Create the user**

```bash
# Windows
venv\Scripts\python manage.py createsuperuser

# Linux / macOS
venv/bin/python manage.py createsuperuser
```

The password must have at least 8 characters, an uppercase letter, a lowercase letter, a digit and a special character (for example `Admin@123`).

**2. Give that user the admin role.** Replace `admin` with the username you chose:

```bash
# Windows
venv\Scripts\python manage.py shell -c "from accounts.models import User; User.objects.filter(username='admin').update(role='admin')"

# Linux / macOS
venv/bin/python manage.py shell -c "from accounts.models import User; User.objects.filter(username='admin').update(role='admin')"
```

You can also do this from the Django admin panel. Log in at **http://127.0.0.1:8000/admin/**, open **Users**, select the user, set **Role** to *Admin* under **Hotel Info**, and save.

---

## Using the App

| Page | URL | Who |
|------|-----|-----|
| Home | `/` | Everyone |
| Register / Login | `/accounts/register/`, `/accounts/login/` | Everyone |
| Room list | `/rooms/` | Everyone |
| Dashboard | `/dashboard/` | Logged-in users (content depends on role) |
| My bookings | `/bookings/` | Guests see their own, admins see all |
| Profile | `/accounts/profile/` | Logged-in users |
| Add / edit / delete rooms | `/rooms/create/` | Admin |
| Audit log | `/audit/` | Admin |
| Django admin panel | `/admin/` | Superuser |

**Roles**

| Role  | Access |
|-------|--------|
| Admin | Full access: rooms, all bookings, booking status, audit logs |
| Guest | Browse rooms, manage own bookings, edit profile |

New accounts created through the **Register** page are always guests.

**Getting started:** the database starts empty except for the room types. Log in as admin, add a few rooms with photos using **Add Room** in the navigation menu or **Add New Room** on the admin dashboard, then register a separate guest account to try booking them.

---

## Manual Setup

If you prefer not to use the setup script:

```bash
cd veloria_grand_hotel/veloria
python -m venv venv

venv\Scripts\activate            # Windows
source venv/bin/activate         # Linux / macOS

pip install -r requirements.txt
copy .env.example .env           # Windows
cp .env.example .env             # Linux / macOS
```

Open `.env` and replace the `SECRET_KEY` value with a random string. You can generate one with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then:

```bash
python manage.py migrate         # creates the database and default room types
python manage.py createsuperuser
python manage.py runserver
```

Remember to [give your user the admin role](#creating-an-admin-account).

---

## Configuration

All settings are in `veloria/.env`, which the setup script creates from [`.env.example`](veloria/.env.example). The most useful ones:

| Variable | Default | Meaning |
|----------|---------|---------|
| `SECRET_KEY` | generated | Django secret key. Keep it private and never commit it. |
| `DEBUG` | `True` | Shows detailed error pages. Set to `False` in production. |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Hostnames the app will serve |
| `MAX_LOGIN_ATTEMPTS` | `5` | Failed logins before an account is locked |
| `LOCKOUT_DURATION_MINUTES` | `30` | How long a locked account stays locked |
| `MAX_UPLOAD_SIZE_MB` | `5` | Maximum image upload size |
| `EMAIL_BACKEND` | console | Emails are printed in the terminal instead of being sent |

**Not in this repository:** `.env`, `db.sqlite3`, `media/` (uploaded photos) and `logs/`. Each person who clones the project gets their own local database, uploads and logs.

**Deploying behind HTTPS:** set `DEBUG=False` and set `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` and `SECURE_SSL_REDIRECT` to `True`. Set `SECURE_HSTS_SECONDS` to a positive value such as `31536000`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python` is not recognized | Install Python and tick **"Add Python to PATH"** during installation, then open a new terminal. |
| `./setup.sh: Permission denied` | Run `chmod +x setup.sh` first, or use `bash setup.sh`. |
| `UndefinedValueError: SECRET_KEY not found` | `.env` is missing. Run the setup script again, or copy `.env.example` to `.env`. |
| Admin user can't add rooms or see the audit log | The user still has the `guest` role. See [Creating an Admin Account](#creating-an-admin-account). |
| "Account locked" after wrong passwords | Wait 30 minutes, or unlock the user in `/admin/` by clearing **Lockout until** and setting **Failed login attempts** to 0. |
| Logged out automatically | Sessions expire after 30 minutes of inactivity, or when the browser is closed. This is intended. |
| Port 8000 already in use | Run on another port: `python manage.py runserver 8080` |
| Want to start fresh | Stop the server, delete `db.sqlite3` and `media/`, then run `python manage.py migrate`. |

---

## Security Features

- OWASP Top 10 compliant
- Argon2 password hashing
- Strong password policy (length, upper/lowercase, digit, special character)
- CSRF protection on all forms
- Role-Based Access Control (Admin / Guest)
- Session timeout (30 minutes)
- Input validation (whitelist + regex)
- File upload security (MIME check, UUID rename, size limit)
- Audit logging for all security events
- Custom error pages (400, 403, 404, 500)
- XSS prevention via Django auto-escaping
- IDOR prevention on all endpoints
- Account lockout after 5 failed login attempts
- Secure headers (X-Frame-Options DENY, nosniff, strict referrer policy)

---

## Tech Stack

- **Framework:** Django 4.2
- **Language:** Python 3.10+
- **Database:** SQLite (development)
- **Frontend:** Bootstrap 5, Font Awesome, django-crispy-forms
- **Password Hashing:** Argon2

---

## Project Structure

```
veloria_grand_hotel/
├── README.md
└── veloria/                 # Django project (run all commands from here)
    ├── config/              # Settings, URLs, WSGI
    ├── accounts/            # Auth, RBAC, profiles, lockout, password validator
    ├── rooms/               # Room management (CRUD)
    ├── bookings/            # Booking system (CRUD)
    ├── audit/               # Audit logging
    ├── hotel/               # Home, dashboards, error pages
    ├── templates/           # HTML templates
    ├── static/              # CSS, JS, images
    ├── .env.example         # Environment template
    ├── requirements.txt     # Dependencies
    ├── setup.bat / setup.sh # One-time setup scripts
    └── manage.py
```

---

## Course Information

- **Course:** IKB21503 Secure Software Development
- **Institution:** Universiti Kuala Lumpur (UniKL MIIT)
- **Semester:** 2025/October
