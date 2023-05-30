from rest_framework import serializers


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ObtainTokenOTPSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6)
