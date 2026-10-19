from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class User(AbstractUser):
    ROLE_GUEST = 'guest'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_GUEST, 'Guest'),
        (ROLE_ADMIN, 'Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_GUEST)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts_user'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin_user(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_locked_out(self):
        if self.lockout_until and timezone.now() < self.lockout_until:
            return True
        return False

    def increment_failed_login(self):
        from django.conf import settings
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            self.lockout_until = timezone.now() + timezone.timedelta(
                minutes=settings.LOCKOUT_DURATION_MINUTES
            )
        self.save(update_fields=['failed_login_attempts', 'lockout_until'])

    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.lockout_until = None
        self.save(update_fields=['failed_login_attempts', 'lockout_until'])
