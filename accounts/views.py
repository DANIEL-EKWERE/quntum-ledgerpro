from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm, UserDataForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('user_data')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def user_data(request):
    # Skip if already filled in
    if request.user.country and request.user.phone:
        return redirect('user_dashboard')
    form = UserDataForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile setup complete. Welcome!')
        return redirect('user_dashboard')
    return render(request, 'accounts/user-data.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get('next', 'user_dashboard'))
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def password_reset(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(request=request)
        messages.success(request, 'Password reset email sent.')
        return redirect('login')
    return render(request, 'accounts/password-reset.html', {'form': form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated.')
        return redirect('profile')
    return render(request, 'dashboard/profile.html', {'form': form})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully.')
        return redirect('change_password')
    return render(request, 'dashboard/change-password.html', {'form': form})
