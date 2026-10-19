from .models import log_action, AuditLog
import logging

logger = logging.getLogger('audit')


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log access denied responses
        if response.status_code == 403 and request.user.is_authenticated:
            log_action(
                user=request.user,
                action=AuditLog.ACTION_ACCESS_DENIED,
                description=f'Access denied to: {request.path}',
                request=request,
            )
            logger.warning(f'Access denied: {request.user.username} -> {request.path}')

        return response
