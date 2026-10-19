from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from rooms.models import Room, RoomType
from bookings.models import Booking
from accounts.models import User


def home(request):
    featured_rooms = Room.objects.filter(status='available').select_related('room_type')[:6]
    room_types = RoomType.objects.all()
    return render(request, 'hotel/home.html', {
        'featured_rooms': featured_rooms,
        'room_types': room_types,
    })


@login_required
def dashboard(request):
    if request.user.is_admin_user:
        total_rooms = Room.objects.count()
        available_rooms = Room.objects.filter(status='available').count()
        total_bookings = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        total_guests = User.objects.filter(role='guest').count()
        recent_bookings = Booking.objects.select_related('user', 'room').order_by('-created_at')[:5]
        context = {
            'total_rooms': total_rooms,
            'available_rooms': available_rooms,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'total_guests': total_guests,
            'recent_bookings': recent_bookings,
        }
        return render(request, 'hotel/admin_dashboard.html', context)
    else:
        my_bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-created_at')[:5]
        available_rooms = Room.objects.filter(status='available').select_related('room_type')[:4]
        context = {
            'my_bookings': my_bookings,
            'available_rooms': available_rooms,
        }
        return render(request, 'hotel/guest_dashboard.html', context)


def error_400(request, exception=None):
    content = render_to_string('errors/400.html', {})
    return HttpResponse(content, status=400)

def error_403(request, exception=None):
    content = render_to_string('errors/403.html', {})
    return HttpResponse(content, status=403)

def error_404(request, exception=None):
    content = render_to_string('errors/404.html', {})
    return HttpResponse(content, status=404)

def error_500(request):
    content = render_to_string('errors/500.html', {})
    return HttpResponse(content, status=500)


# Test views to trigger error handlers
def test_error_400(request):
    raise SuspiciousOperation("Test 400 error")

def test_error_403(request):
    raise PermissionDenied("Test 403 error")

def test_error_404(request):
    raise Http404("Test 404 error")

def test_error_500(request):
    raise Exception("Test 500 error")
