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
        discounted_price = serializer.validated_data.get('discounted_price')
        image = serializer.validated_data.get('image')
        if discounted_price != "None":
            temp_dict = {'pk': pk, 'name': name.encode('utf-8'), 'price': discounted_price, 'image': image, 'count': 1}
        else:
            temp_dict = {'pk': pk, 'name': name.encode('utf-8'), 'price': price, 'image': image, 'count': 1}

        cart = request.COOKIES.get('cart', None)
        if not cart:
            cart = f'{temp_dict}'
        else:
            cart += f';{temp_dict}'

        response = Response({'cart': 'ok'})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("cart", cart, expires=expires_string)

        return response
