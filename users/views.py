from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.db import transaction

from users.models import UserProfile
from users.forms import UserRegisterForm, UserLoginForm

User = get_user_model()

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = User(
                    email=form.cleaned_data.get('email'),
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                )
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                user_profile = UserProfile.objects.create(
                    user=user,
                    user_type=form.cleaned_data.get('type'),
                    bio=form.cleaned_data.get('bio'),
                    photo=form.cleaned_data.get('photo')
                )
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data.get('email')).first()
            login(request, user)
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
