from rest_framework import serializers
from user.models import User, Address


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday', 'gender', 'profile_pic']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['pk', 'province', 'city', 'address', 'postal_code']
