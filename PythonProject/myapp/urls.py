from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('listing/', views.listing, name='listing'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
]
