import os
import uuid
from django import forms
from django.conf import settings
from .models import Room, RoomType


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'description', 'price_per_night', 'capacity', 'status', 'image', 'amenities', 'floor']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'amenities': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WiFi, TV, Air Conditioning'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            if image.size > settings.MAX_UPLOAD_SIZE_BYTES:
                raise forms.ValidationError('Image must not exceed 5MB.')
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
            image.name = f"{uuid.uuid4().hex}{ext}"
        return image

    def clean_price_per_night(self):
        price = self.cleaned_data.get('price_per_night')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_room_number(self):
        number = self.cleaned_data.get('room_number', '')
        import re
        if not re.match(r'^[A-Za-z0-9\-]+$', number):
            raise forms.ValidationError('Room number can only contain letters, numbers, and hyphens.')
        return number
