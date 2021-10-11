from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.views.generic import DetailView
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


class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'users/profile.html'