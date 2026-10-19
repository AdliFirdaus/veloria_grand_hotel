from django.conf import settings

def site_settings(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'ADMIN_EMAIL': settings.ADMIN_EMAIL,
    }
