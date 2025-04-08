from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'RegisterPage.html')

def login(request):
    return render(request, 'LoginPage.html')    return render(request, 'LoginPage.html')

def listing(request):
    return render(request, 'listing_list.html')

def profile(request):
    return render(request, 'profile.html')

def edit(request):
    return render(request, 'edit_list.html')

def create(request):
    return render(request, 'creeate_listing.html')

