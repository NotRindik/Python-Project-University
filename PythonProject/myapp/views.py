from . import forms
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Listing
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, ListingForm, CustomAuthenticationForm


def home(request):
    listing_page = Listing.objects.all()
    return render(request, 'home.html', {'listing': listing_page})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, "RegisterPage.html", {"form": form})

def login(request):
    if request.method == "POST":
        form = forms.CustomAuthenticationForm(data=request.POST)
        form.request = request
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'LoginPage.html', {'form': form})


def listing(request):
    return render(request, 'listing_list.html')

def listing_detail(request, listing_id):
    listing_page = get_object_or_404(Listing, id=listing_id)
    return render(request, 'listing_page.html', {'listing': listing_page})

@login_required
@login_required
def profile(request):
    user = request.user
    user_listings = Listing.objects.filter(user=user)

    context = {
        'user_name': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'avatar': user.avatar.url if user.avatar else None,
        'is_verified': user.is_verified,
        'user_listings': user_listings,
    }
    return render(request, 'profile.html', context)


def edit(request):
    return render(request, 'edit_listing.html')

def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()

    return render(request, 'creeate_listing.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, user=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'edit_listing.html', {'form': form, 'listing': listing})


from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        'Тестовое письмо',
        'Если ты видишь это письмо — значит все работает!',
        '41059@iitu.edu.kz',           # from
        ['41059@iitu.edu.kz'],
        fail_silently=False,
    )
    return HttpResponse("Письмо отправлено!")