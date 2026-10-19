import logging
import uuid
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .forms import LoginForm, RegisterForm, ProfileUpdateForm
from .models import User

logger = logging.getLogger('accounts')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('hotel:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username', '')[:150]

        try:
            user_obj = User.objects.get(username=username)
            if user_obj.is_locked_out:
                messages.error(request, 'Account locked due to too many failed attempts. Try again later.')
                logger.warning(f'Locked account login attempt: {username}')
                return render(request, 'accounts/login.html', {'form': form})
        except User.DoesNotExist:
            pass

        if form.is_valid():
            user = form.get_user()
            user.reset_failed_login()
            login(request, user)
            request.session['last_activity'] = timezone.now().isoformat()
            logger.info(f'Successful login: {user.username} | Role: {user.role}')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', '')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('hotel:dashboard')
        else:
            try:
                user_obj = User.objects.get(username=username)
                user_obj.increment_failed_login()
                logger.warning(f'Failed login attempt: {username} | Attempts: {user_obj.failed_login_attempts}')
            except User.DoesNotExist:
                logger.warning(f'Failed login attempt for non-existent user: {username}')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('hotel:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.ROLE_GUEST
            user.save()
            logger.info(f'New user registered: {user.username}')
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        logger.info(f'User logged out: {username}')
        messages.success(request, 'You have been logged out successfully.')
    return redirect('hotel:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                pic = request.FILES['profile_picture']
                ext = os.path.splitext(pic.name)[1].lower()
                pic.name = f"{uuid.uuid4().hex}{ext}"
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
