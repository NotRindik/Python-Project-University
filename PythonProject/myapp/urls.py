from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('listing/', views.listing, name='listing'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('logout/', logout_view, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
