from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect("home")  # Замени на свою главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, "RegisterPage.html", {"form": form})

def login(request):
    return render(request, 'LoginPage.html')

def listing(request):
    return render(request, 'listing_list.html')

def profile(request):
    return render(request, 'profile.html')

def edit(request):
    return render(request, 'edit_list.html')

def create(request):
    return render(request, 'creeate_listing.html')

