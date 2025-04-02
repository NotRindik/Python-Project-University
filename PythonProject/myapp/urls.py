from django.urls import path

from . import views


urlpatterns = [

path('', views.home, name='home'),
    path('register/', views.register, name='RegisterPage'),  # Уникальный URL
    path('login/', views.login, name='LoginPage'),
]