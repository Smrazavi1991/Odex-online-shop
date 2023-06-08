from rest_framework import serializers
from user.models import User, Address
from order.models import Order, Cart
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
    address = UserAddressSerializer()

    class Meta:
        model = Cart
        fields = ['customer', 'item', 'shipping_price', 'address', 'total_price']


class UserOrderSerializer(serializers.ModelSerializer):
    cart_id = UserCartSerializer()

    class Meta:
        model = Order
        fields = ['create_date', 'cart_id', 'status']
