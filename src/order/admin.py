from django.contrib import admin
from .models import *


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'shipping_price', 'customer_id', 'last_change', 'is_deleted')
    search_fields = ("item", )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_id', 'status', 'last_change', 'is_deleted')


class DiscountCouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'discount_id', 'owner_id', 'discount_is_active', 'last_change', 'is_deleted')
    search_fields = ("code",)


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DiscountCoupon, DiscountCouponAdmin)
