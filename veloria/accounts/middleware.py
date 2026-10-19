from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.conf import settings


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                elapsed = (timezone.now() - timezone.datetime.fromisoformat(last_activity)).seconds
                if elapsed > settings.SESSION_COOKIE_AGE:
                    from django.contrib.auth import logout
                    logout(request)
                    messages.warning(request, 'Your session has expired. Please log in again.')
                    return redirect(settings.LOGIN_URL)
            request.session['last_activity'] = timezone.now().isoformat()
        return self.get_response(request)
