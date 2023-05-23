from django.contrib import admin
from .models import *


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
    list_display = ('id', 'name', 'brand', 'count', 'price', 'discount_is_active', 'img_preview', 'is_deleted')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'discount_is_active', 'last_change', 'is_deleted')


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'is_approved', 'owner_id', 'product_id', 'last_change', 'is_deleted')


class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
    list_display = ('id', 'product_id', 'last_change', 'img_preview', 'is_deleted')


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount_of_percentage_discount', 'amount_of_non_percentage_discount', 'last_change', 'is_deleted')


class InformationItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_change', 'is_deleted')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(InformationItem, InformationItemAdmin)
