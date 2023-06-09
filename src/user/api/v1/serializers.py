from rest_framework import serializers
from user.models import User, Address
from order.models import Order, Cart
from product.models import Product
from core.views import ProductsViewMixin
from django_jalali.serializers.serializerfield import JDateField


class UserInformationSerializer(serializers.ModelSerializer):
    birthday = JDateField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday', 'gender', 'profile_pic']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['pk', 'province', 'city', 'address', 'postal_code']


class UserCartSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer(required=True)
    shipping_method = serializers.SerializerMethodField()
    cart_item_pics = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['customer', 'item', 'shipping_price', 'address', 'total_price', 'shipping_method', 'cart_item_pics']

    def get_shipping_method(self, obj):
        if obj.shipping_price == "18000 تومان":
            shipping_method = "ارسال اکسپرس (تحویل در 3 - 5 روز کاری)"
        else:
            shipping_method = "ارسال معمولی (تحویل در 5 - 7 روز کاری)"
        return shipping_method

    def get_cart_item_pics(self, obj):
        print(type(obj.item))
        for i in obj.item:
            product = Product.objects.get(pk=i.pk)
            if obj.item.index(i) == 0:
                pic = ProductsViewMixin.get_pics_from_a_product_queryset(product, is_primary=True)
            else:
                pic.append(ProductsViewMixin.get_pics_from_a_product_queryset(product, is_primary=True))
        return pic


class UserOrderSerializer(serializers.ModelSerializer):
    cart = UserCartSerializer(required=True)
    create_date = JDateField(format='%Y-%m-%d')

    class Meta:
        model = Order
        fields = ['pk', 'create_date', 'cart', 'status']
