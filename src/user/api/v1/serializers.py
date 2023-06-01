from rest_framework import serializers
from user.models import User


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'birthday', 'gender', 'profile_pic', 'is_active']
