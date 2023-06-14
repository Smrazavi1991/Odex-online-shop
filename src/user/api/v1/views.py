from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.status import HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.authentication import JWTAuthentication

from .serializers import *
from user.models import User, Address
from order.models import Order
from product.models import Product
from core.views import ProductsViewMixin


class ObtainTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = None

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
        return Response(serializer_.data)


class UserOrderPics(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserOrderPicsSerializer

    def get(self, request, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        items = order.cart.item
        for i in items:
            product = Product.objects.filter(pk=i['pk'])
            if items.index(i) == 0:
                pic = ProductsViewMixin.get_pics_from_a_product_queryset(product, is_primary=True)
            else:
                temp = ProductsViewMixin.get_pics_from_a_product_queryset(product, is_primary=True)
                pic.append(temp[0])
        serializer_ = self.serializer_class(pic, many=True)
        return Response(serializer_.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer_ = self.serializer_class(data=request.data)
        serializer_.is_valid(raise_exception=True)
        username = self.request.session.get('username', None)
        user = User.objects.get(username=username)
        if check_password(serializer_.validated_data['oldpassword'], user.password):
            user.password = make_password(serializer_.validated_data['newpassword'])
            user.save()
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'failed'}, status=HTTP_406_NOT_ACCEPTABLE)


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
        user.address.create(province=serializer_.validated_data['province'], city=serializer_.validated_data['city'],
                            address=serializer_.validated_data['address'],
                            postal_code=serializer_.validated_data['postal_code'])
        return Response({'status': 'ok'})


class RemoveAddress(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def delete(self, request, **kwargs):
        address_object = get_object_or_404(Address, pk=self.kwargs['pk'])
        address_object.is_deleted = True
        address_object.save()
        return Response({'status': 'ok'})
