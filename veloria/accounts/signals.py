from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
import logging

logger = logging.getLogger('accounts')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f'Login success: {user.username}')

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    logger.warning(f'Login failed for: {credentials.get("username", "unknown")}')
