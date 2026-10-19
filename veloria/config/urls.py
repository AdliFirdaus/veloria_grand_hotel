from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hotel.urls', namespace='hotel')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('rooms/', include('rooms.urls', namespace='rooms')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('audit/', include('audit.urls', namespace='audit')),
]

# Serve media files
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Serve static files
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]
