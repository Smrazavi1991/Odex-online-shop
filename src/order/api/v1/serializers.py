from rest_framework import serializers


class AddToCartViewSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.CharField()
    discounted_price = serializers.CharField()


class RemoveFromCartViewSerializer(serializers.Serializer):
    pk = serializers.CharField()


class UpdateCartSerializer(serializers.Serializer):
    pk = serializers.CharField()
    name = serializers.CharField(max_length=100)
    price = serializers.CharField()
    discounted_price = serializers.CharField()
    count = serializers.IntegerField()
    image = serializers.ImageField()