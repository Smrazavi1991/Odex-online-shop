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


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'city', 'address', 'postal_code', 'last_change', 'is_deleted')


admin.site.register(User, UsersAdmin)
admin.site.register(Address, AddressAdmin)
