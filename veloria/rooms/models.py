from django.db import models
import uuid


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        ('occupied', 'Occupied'),
        (STATUS_MAINTENANCE, 'Under Maintenance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    amenities = models.TextField(blank=True, help_text='Comma separated amenities')
    floor = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_number']

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type.name}"

    def get_amenities_list(self):
        if self.amenities:
            return [a.strip() for a in self.amenities.split(',') if a.strip()]
        return []
