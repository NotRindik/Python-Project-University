from .models import Task
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Listing
from django.utils.translation import gettext_lazy as _
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'groups')

    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('first_name', 'last_name', 'email')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'avatar', 'password1', 'password2', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'category', 'created_at')
    list_filter = ('category', 'price')
    search_fields = ('title', 'description', 'user__email')
    ordering = ('-created_at',)

#admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Listing, ListingAdmin)