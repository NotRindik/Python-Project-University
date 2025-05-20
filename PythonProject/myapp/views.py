from . import forms
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Listing
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, ListingForm, CustomAuthenticationForm
from django.http import HttpResponseForbidden
from .forms import ProfileUpdateForm

def home(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    listings = Listing.objects.order_by('-created_at')

    if category:
        listings = listings.filter(category=category)

    if query:
        listings = listings.filter(title__icontains=query)

    context = {
        'listing': listings,
        'query': query,
        'category': category,
    }
    return render(request, 'home.html', context)

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

import random
from django.shortcuts import render, redirect
from .models import CustomUser

def send_code(request):
    code = str(random.randint(1000, 9999))
    request.session['email_code'] = code
    request.session['email_verified'] = False
    user = CustomUser.objects.get(id=request.user.id)

    send_mail(
        'Ваш код подтверждения',
        f'Введите этот код: {code}',
        '41059@iitu.edu.kz',
        [user.email],
        fail_silently=False,
    )

    return redirect('verify_email_form')


def verify_email_form(request):
    return render(request, 'verify_email.html')

def chat_list_view(request):
    current_user = request.user
    chat_users = get_chat_users_for(current_user)

    listing_user_id = request.GET.get("user_id")
    if listing_user_id:
        try:
            extra_user = CustomUser.objects.get(id=listing_user_id)
            if extra_user not in chat_users:
                chat_users = list(chat_users) + [extra_user]
        except CustomUser.DoesNotExist:
            pass

    return render(request, 'chat.html', {'chat_users': chat_users})

def confirm_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('code')
        session_code = request.session.get('email_code')

        if input_code == session_code:
            request.session['email_verified'] = True
            request.user.is_verified = True
            request.user.save()
            return redirect('/profile/')
        else:
            return render(request, 'verify_email.html', {'error': 'Неверный код'})

    return redirect('verify_email_form')

from .models import Message, CustomUser
def get_chat_users_for(current_user):
    sent = Message.objects.filter(sender=current_user).values_list('recipient', flat=True)
    received = Message.objects.filter(recipient=current_user).values_list('sender', flat=True)

    user_ids = set(sent).union(received)
    return CustomUser.objects.filter(id__in=user_ids)

from django.db.models import Q
from .forms import MessageForm
@login_required
def chat_detail_view(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(CustomUser, id=user_id)
    if current_user == other_user:
        print(f'{current_user.id} and {other_user.id} is Fucking EEqual')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_msg = form.save(commit=False)
            new_msg.sender = current_user
            new_msg.recipient = other_user
            new_msg.save()
            return redirect(f'/profile/chat/{other_user.id}/', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'chat_detail.html', {
        'form': form,
        'other_user': other_user,
    })

from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Message

@login_required
def chat_messages_ajax(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(
        Q(sender=current_user, recipient=other_user) |
        Q(sender=other_user, recipient=current_user)
    ).order_by('timestamp')
    html = render_to_string('messages.html', {'messages': messages,'request': request})
    return JsonResponse({'html': html})

def delete_listing(request,pk):
    listing = get_object_or_404(Listing, id=pk)
    if listing.user != request.user:
        return HttpResponseForbidden("Вы не можете удалить это объявление.")

    if request.method == "POST":
        listing.delete()
        return redirect('profile')

    return redirect('profile')

def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})

