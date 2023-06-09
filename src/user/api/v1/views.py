from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.authentication import JWTAuthentication
import datetime

from .serializers import *
from user.models import User, Address
from order.models import Order, Cart


class ObtainTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = self.request.session.get('username', None)
        if user:
            # Generate the JWT token
            jwt_token = JWTAuthentication.create_jwt(user)

            response = Response({'token': jwt_token})
            expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
            expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
            response.set_cookie("token", jwt_token, expires=expires_string)

            return response
        else:
            raise AuthenticationFailed('Invalid username')


class UserInformation(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get(self, request):
        username = self.request.session['username']
        user = User.objects.get(username=username)
        serializer_ = self.serializer_class(user)
        return Response(serializer_.data)

    def patch(self, request):
        username = self.request.session['username']
        user = User.objects.get(username=username)
        serializer_ = self.serializer_class(user, data=request.data, partial=True)
        serializer_.is_valid(raise_exception=True)
        serializer_.save()
        return Response(serializer_.data)


class UserOrdersList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserOrderSerializer

    def get(self, request):
        username = self.request.session['username']
        user = User.objects.get(username=username)
        order = Order.objects.filter(cart__customer_id=user.pk)
        serializer_ = self.serializer_class(order, many=True)
        return Response(serializer_.data)


class UserOrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserOrderSerializer

    def get(self, request, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        serializer_ = self.serializer_class(order)
        print(serializer_.data)
        return Response(serializer_.data)


class ChangePassword(APIView):
    pass


class UserAddress(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer

    def get(self, request):
        username = self.request.session.get('username', None)
        user = User.objects.get(username=username)
        condition1 = Q(user__id=user.pk)
        condition2 = Q(is_deleted=False)
        user_address = Address.objects.filter(condition1 & condition2)
        serializer_ = self.serializer_class(user_address, many=True)
        return Response(serializer_.data)

    def post(self, request):
        serializer_ = self.serializer_class(data=request.data)
        serializer_.is_valid(raise_exception=True)
        username = self.request.session.get('username', None)
        user = User.objects.get(username=username)
        user.address.create(province=serializer_.validated_data['province'], city=serializer_.validated_data['city'], address=serializer_.validated_data['address'], postal_code=serializer_.validated_data['postal_code'])
        return Response({'status': 'ok'})

    # def patch(self, request):
    #     pass