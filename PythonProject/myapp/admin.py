

from .models import Task
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Listing
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Поля, которые будут
    search_fields = ('title',)  # Поиск по названию задачи
    list_filter = ('created_at',)  # Фильтр по дате создания
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'email', 'phone', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('first_name','last_name', 'email', 'phone')
    ordering = ('first_name','last_name','email',)

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'category', 'created_at')
    list_filter = ('category', 'price')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Listing, ListingAdmin)