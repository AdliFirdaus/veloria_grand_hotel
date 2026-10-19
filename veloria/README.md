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
- **Language:** Python 3.11
- **Database:** SQLite (development)
- **Frontend:** Bootstrap 5, Font Awesome
- **Password Hashing:** Argon2

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd veloria
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create admin user
```bash
python manage.py createsuperuser
```

### 7. Create initial room types (optional)
```bash
python manage.py shell
>>> from rooms.models import RoomType
>>> RoomType.objects.create(name='Deluxe Room', description='Spacious deluxe room')
>>> RoomType.objects.create(name='Executive Suite', description='Premium executive suite')
>>> RoomType.objects.create(name='Presidential Suite', description='Top floor presidential suite')
```

### 8. Run the server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

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
