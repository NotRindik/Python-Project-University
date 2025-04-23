from django.contrib.auth.views import LogoutView
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
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listing/edit/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
