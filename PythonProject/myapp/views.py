from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ListingForm

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "RegisterPage.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "LoginPage.html", {"form": form})


@login_required
def listing(request):
    return render(request, 'listing_list.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def edit(request):
    return render(request, 'edit_list.html')


@login_required
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('listing')
    else:
        form = ListingForm()
    return render(request, 'creeate_listing.html', {'form': form})