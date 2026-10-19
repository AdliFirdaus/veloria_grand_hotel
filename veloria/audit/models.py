from django.db import models
from django.conf import settings
import uuid


class AuditLog(models.Model):
    ACTION_LOGIN = 'LOGIN'
    ACTION_LOGOUT = 'LOGOUT'
    ACTION_LOGIN_FAILED = 'LOGIN_FAILED'
    ACTION_BOOKING_CREATE = 'BOOKING_CREATE'
    ACTION_BOOKING_CANCEL = 'BOOKING_CANCEL'
    ACTION_BOOKING_UPDATE = 'BOOKING_UPDATE'
    ACTION_ROOM_CREATE = 'ROOM_CREATE'
    ACTION_ROOM_UPDATE = 'ROOM_UPDATE'
    ACTION_ROOM_DELETE = 'ROOM_DELETE'
    ACTION_PROFILE_UPDATE = 'PROFILE_UPDATE'
    ACTION_ACCESS_DENIED = 'ACCESS_DENIED'
    ACTION_ADMIN = 'ADMIN_ACTION'

    ACTION_CHOICES = [
        (ACTION_LOGIN, 'Login'),
        (ACTION_LOGOUT, 'Logout'),
        (ACTION_LOGIN_FAILED, 'Login Failed'),
        (ACTION_BOOKING_CREATE, 'Booking Created'),
        (ACTION_BOOKING_CANCEL, 'Booking Cancelled'),
        (ACTION_BOOKING_UPDATE, 'Booking Updated'),
        (ACTION_ROOM_CREATE, 'Room Created'),
        (ACTION_ROOM_UPDATE, 'Room Updated'),
        (ACTION_ROOM_DELETE, 'Room Deleted'),
        (ACTION_PROFILE_UPDATE, 'Profile Updated'),
        (ACTION_ACCESS_DENIED, 'Access Denied'),
        (ACTION_ADMIN, 'Admin Action'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='audit_logs'
    )
    username = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.action} - {self.username}"


def log_action(user=None, action='', description='', request=None, extra_data=None):
    ip = None
    ua = ''
    if request:
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded.split(',')[0].strip() if x_forwarded else request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')[:300]

    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        username=user.username if user and user.is_authenticated else 'anonymous',
        action=action,
        description=description,
        ip_address=ip,
        user_agent=ua,
        extra_data=extra_data or {},
    )
