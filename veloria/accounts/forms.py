import re

import os
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        max_length=150,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        # Whitelist: only alphanumeric, underscore, hyphen, dot
        if not re.match(r'^[\w.\-@+]+$', username):
            raise forms.ValidationError('Invalid username format.')
        return username


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    phone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (optional)'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone and not re.match(r'^\+?[\d\s\-]{7,20}$', phone):
            raise forms.ValidationError('Enter a valid phone number.')
        return phone

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name', '')
        if not re.match(r'^[a-zA-Z\s\-]+$', name):
            raise forms.ValidationError('Name can only contain letters, spaces, and hyphens.')
        return name

    def clean_last_name(self):
        name = self.cleaned_data.get('last_name', '')
        if not re.match(r'^[a-zA-Z\s\-]+$', name):
            raise forms.ValidationError('Name can only contain letters, spaces, and hyphens.')
        return name


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > settings.MAX_UPLOAD_SIZE_BYTES:
                raise forms.ValidationError(f'File size must not exceed {settings.MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB.')
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError('Only JPG, PNG, and WEBP files are allowed.')
        return picture
