from django.contrib import admin
from .models import Room, RoomType

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'price_per_night', 'status', 'capacity']
    list_filter = ['status', 'room_type']
    search_fields = ['room_number']
