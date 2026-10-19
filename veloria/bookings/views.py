import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from rooms.models import Room
from .models import Booking
from .forms import BookingForm, BookingStatusForm

logger = logging.getLogger('bookings')


@login_required
def booking_create(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk, status='available')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room

            # Check for conflicting bookings
            conflicts = Booking.objects.filter(
                room=room,
                status__in=['pending', 'confirmed'],
                check_in_date__lt=booking.check_out_date,
                check_out_date__gt=booking.check_in_date,
            )
            if conflicts.exists():
                messages.error(request, 'Room is not available for the selected dates.')
            else:
                booking.save()
                logger.info(f'New booking: {booking.id} by {request.user.username}')
                messages.success(request, 'Booking created successfully!')
                return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form, 'room': room})


@login_required
def booking_list(request):
    if request.user.is_admin_user:
        bookings = Booking.objects.all().select_related('user', 'room')
    else:
        bookings = Booking.objects.filter(user=request.user).select_related('room')

    paginator = Paginator(bookings, 10)
    page = request.GET.get('page', '1')
    page = page if page.isdigit() else '1'
    bookings_page = paginator.get_page(int(page))
    return render(request, 'bookings/booking_list.html', {'bookings': bookings_page})


@login_required
def booking_detail(request, pk):
    if request.user.is_admin_user:
        booking = get_object_or_404(Booking, pk=pk)
    else:
        # Prevent IDOR — guest can only see own bookings
        booking = get_object_or_404(Booking, pk=pk, user=request.user)

    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:booking_detail', pk=pk)

    if request.method == 'POST':
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        logger.info(f'Booking cancelled: {booking.id} by {request.user.username}')
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:booking_list')

    return render(request, 'bookings/booking_cancel.html', {'booking': booking})


@login_required
def booking_update_status(request, pk):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('bookings:booking_list')

    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            logger.info(f'Booking status updated: {booking.id} by admin {request.user.username}')
            messages.success(request, 'Booking status updated.')
            return redirect('bookings:booking_detail', pk=pk)
    else:
        form = BookingStatusForm(instance=booking)

    return render(request, 'bookings/booking_status_form.html', {'form': form, 'booking': booking})
