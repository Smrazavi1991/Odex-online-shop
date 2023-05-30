from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        ('date', JDateFieldListFilter),
    )


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'gender', 'email', 'phone', 'birthday',
                    'phone_verified', 'date_joined', 'is_active', 'is_superuser', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    fieldsets = (
        ('Name', {
            'fields': (tuple(['first_name', 'last_name', 'username']),),
        }),
        (None, {
            'fields': (tuple(['email', 'phone', 'phone_verified']),),
        }),
        ('Additional Information', {
            'fields': (tuple(['birthday', 'gender', 'profile_pic']),),
        }),
        (None, {
            'fields': (tuple(['address', 'last_login']),),
        }),
        ('Group and user role info', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Administrative Information', {
            'fields': (tuple(['is_superuser', 'is_staff', 'is_active']),),
        })
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'city', 'address', 'postal_code', 'last_change', 'is_deleted')
    search_fields = ('city', 'address', 'postal_code')


admin.site.register(User, UsersAdmin)
admin.site.register(Address, AddressAdmin)
