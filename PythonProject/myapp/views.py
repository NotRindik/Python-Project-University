from . import forms
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Ad
from .forms import AdForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("home")  # Замени на свою главную страницу
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
                return redirect('home')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = forms.CustomAuthenticationForm()

    return render(request, 'LoginPage.html', {'form': form})

def listing(request):
    ads = Ad.objects.all()
    return render(request, 'listing_list.html', {'ads': ads})  #

@login_required
def profile_view(request):
    user = request.user
    ads_count = user.ads_set.count()

    return render(request, 'profile.html', {
        'user': user,
        'ads_count': ads_count
    })

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('listing')
    else:
        form = AdForm(instance=ad)

    return render(request, 'edit_ad.html', {'form': form})

@login_required
def create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('listing')
    else:
        form = AdForm()

    return render(request, 'create_listing.html', {'form': form})
