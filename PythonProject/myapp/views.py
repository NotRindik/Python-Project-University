from . import forms
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("home")
    else:
        form = forms.CustomUserCreationForm()
    return render(request, "RegisterPage.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = forms.CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # или на нужную страницу после логина
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = forms.CustomAuthenticationForm()

    return render(request, 'LoginPage.html', {'form': form})

def listing(request):
    return render(request, 'listing_list.html')

@login_required
def profile(request):
    user = request.user
    context = {
        'user_name': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'avatar': user.avatar.url if user.avatar else None,
        'is_verified': user.is_verified,
    }
    return render(request, 'profile.html', context)


def edit(request):
    return render(request, 'edit_list.html')

def create(request):
    return render(request, 'creeate_listing.html')

