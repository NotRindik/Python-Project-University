from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect("home")  # Замени на свою главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
