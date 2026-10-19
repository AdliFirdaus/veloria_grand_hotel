from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Room, RoomType
from .forms import RoomForm


def room_list(request):
    rooms = Room.objects.filter(status='available').select_related('room_type')
    room_type_id = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    capacity = request.GET.get('capacity')

    if room_type_id and room_type_id.isdigit():
        rooms = rooms.filter(room_type_id=int(room_type_id))
    if min_price and min_price.replace('.', '').isdigit():
        rooms = rooms.filter(price_per_night__gte=float(min_price))
    if max_price and max_price.replace('.', '').isdigit():
        rooms = rooms.filter(price_per_night__lte=float(max_price))
    if capacity and capacity.isdigit():
        rooms = rooms.filter(capacity__gte=int(capacity))

    paginator = Paginator(rooms, 6)
    page = request.GET.get('page', '1')
    page = page if page.isdigit() else '1'
    rooms_page = paginator.get_page(int(page))
    room_types = RoomType.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms_page, 'room_types': room_types})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_detail.html', {'room': room})


@login_required
def room_create(request):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('rooms:room_list')

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully.')
            return redirect('rooms:room_list')
    else:
        form = RoomForm()
    return render(request, 'rooms/room_form.html', {'form': form, 'action': 'Create'})


@login_required
def room_update(request, pk):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('rooms:room_list')

    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully.')
            return redirect('rooms:room_detail', pk=pk)
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/room_form.html', {'form': form, 'action': 'Update', 'room': room})


@login_required
def room_delete(request, pk):
    if not request.user.is_admin_user:
        messages.error(request, 'Access denied.')
        return redirect('rooms:room_list')

    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted.')
        return redirect('rooms:room_list')
    return render(request, 'rooms/room_confirm_delete.html', {'room': room})
