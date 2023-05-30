import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import AddToCartViewSerializer


class AddToCartView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AddToCartViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        name = serializer.validated_data.get('name')
        price = serializer.validated_data.get('price')
        image = serializer.validated_data.get('image')
        count = serializer.validated_data.get('count')
        temp_dict = {'pk': pk, 'name': name.encode('utf-8'), 'price': price, 'image': image, 'count': count}

        cart = request.COOKIES.get('cart', None)
        if not cart:
            cart = []
        cart.append(temp_dict)

        response = Response({'cart': 'ok'})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("cart", cart, expires=expires_string)

        return response
