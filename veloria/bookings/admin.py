from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price']
    list_filter = ['status']
    search_fields = ['user__username', 'room__room_number']
    readonly_fields = ['id', 'created_at', 'total_price']
