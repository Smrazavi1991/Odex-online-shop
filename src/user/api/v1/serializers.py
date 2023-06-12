from rest_framework import serializers
from user.models import User, Address
from order.models import Order, Cart
from django_jalali.serializers.serializerfield import JDateField


class UserInformationSerializer(serializers.ModelSerializer):
    birthday = JDateField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday', 'gender', 'profile_pic']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['pk', 'province', 'city', 'address', 'postal_code']


class UserCartSerializer(serializers.ModelSerializer):
    address = UserAddressSerializer(required=True)
    shipping_method = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['customer', 'item', 'shipping_price', 'address', 'total_price', 'shipping_method']

    def get_shipping_method(self, obj):
        if obj.shipping_price == "18000 تومان":
            shipping_method = "ارسال اکسپرس (تحویل در 3 - 5 روز کاری)"
        else:
            shipping_method = "ارسال معمولی (تحویل در 5 - 7 روز کاری)"
        return shipping_method


class UserOrderSerializer(serializers.ModelSerializer):
    cart = UserCartSerializer(required=True)
    create_date = JDateField(format='%Y-%m-%d')

    class Meta:
        model = Order
        fields = ['pk', 'create_date', 'cart', 'status']


class UserOrderPicsSerializer(serializers.Serializer):
    id = serializers.CharField()
    image = serializers.ImageField()
