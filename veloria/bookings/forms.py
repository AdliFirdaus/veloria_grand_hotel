from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out:
            if check_in < timezone.now().date():
                raise forms.ValidationError('Check-in date cannot be in the past.')
            if check_out <= check_in:
                raise forms.ValidationError('Check-out date must be after check-in date.')
            if (check_out - check_in).days > 30:
                raise forms.ValidationError('Maximum booking duration is 30 nights.')
        return cleaned_data

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests and (guests < 1 or guests > 10):
            raise forms.ValidationError('Number of guests must be between 1 and 10.')
        return guests

    def clean_special_requests(self):
        text = self.cleaned_data.get('special_requests', '')
        # Strip any HTML tags for XSS prevention
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text[:500]


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
