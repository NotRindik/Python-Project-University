

from .models import Task
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Ad
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Поля, которые будут
    search_fields = ('title',)  # Поиск по названию задачи
    list_filter = ('created_at',)  # Фильтр по дате создания
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'category', 'created_at')
    list_filter = ('category', 'price')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Ad, ListingAdmin)