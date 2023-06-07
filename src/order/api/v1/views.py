import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound

from .serializers import *
from ...models import DiscountCoupon
from user.models import User
from core.views import BasicViewMixin


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
        if discounted_price != "None":
            temp_dict = {'pk': pk, 'name': name.encode('utf-8'), 'price': discounted_price, 'count': 1}
        else:
            temp_dict = {'pk': pk, 'name': name.encode('utf-8'), 'price': price, 'count': 1}

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


class RemoveFromCartView(APIView, BasicViewMixin):
    permission_classes = [AllowAny]
    serializer_class = RemoveFromCartViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        pk = serializer.validated_data.get('pk')
        cart = self.get_user_cart(self.request, total=False)
        temp_str = ''
        for product in cart:
            product['image'] = ""
            if product['pk'] == pk:
                del product
                continue
            product['name'] = product['name'].encode('utf-8')
            if len(temp_str) == 0:
                temp_str = f'{product}'
            else:
                temp_str += f';{product}'

        response = Response({'cart': 'ok'})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("cart", temp_str, expires=expires_string)

        return response


class UpdateCart(APIView, BasicViewMixin):
    permission_classes = [AllowAny]
    serializer_class = UpdateCartSerializer

    def get(self, request):
        cart = self.get_user_cart(self.request, total=False)
        serializer_ = self.serializer_class(data=cart, many=True)
        serializer_.is_valid(raise_exception=True)
        return Response(serializer_.data)

    def patch(self, request):
        serializer_ = self.serializer_class(data=request.data, partial=True)
        serializer_.is_valid(raise_exception=True)

        pk = serializer_.validated_data['pk']
        count = serializer_.validated_data['count']
        print(pk, type(pk), count, type(count))
        cart = self.get_user_cart(self.request, total=False)
        temp_str = ''
        for product in cart:
            product['image'] = ""
            if product['pk'] == pk:
                product['count'] = count
            product['name'] = product['name'].encode('utf-8')
            if len(temp_str) == 0:
                temp_str = f'{product}'
            else:
                temp_str += f';{product}'

        response = Response({'cart': 'ok'})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("cart", temp_str, expires=expires_string)

        return response


class CalculateTotal(APIView, BasicViewMixin):
    permission_classes = [AllowAny]
    serializer_class = CalculateTotalSerializer

    def get(self, request):
        totals = self.get_user_cart(self.request, total=True)
        serializer_ = self.serializer_class(data=totals)
        serializer_.is_valid(raise_exception=True)
        return Response(serializer_.data)


class CalculateDiscount(APIView, BasicViewMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CalculateDiscountSerializer
    discount_amount = 0
    shipping_price = 0

    def post(self, request):
        serializer_ = self.serializer_class(data=request.data)
        serializer_.is_valid(raise_exception=True)
        CalculateDiscount.shipping_price = serializer_.validated_data['shipping_price']
        coupon_code = DiscountCoupon.objects.filter(code=serializer_.validated_data['code'])
        if coupon_code:
            username = self.request.session.get('username', None)
            user = User.objects.get(username=username)
            for code in coupon_code:
                if code.discount_is_active and code.owner == user:
                    if code.discount.amount_of_percentage_discount:
                        CalculateDiscount.discount_amount = code.discount.amount_of_percentage_discount
                        response = Response({'value': CalculateDiscount.discount_amount})
                    else:
                        CalculateDiscount.discount_amount = code.discount.amount_of_non_percentage_discount
                        response = Response({'value': CalculateDiscount.discount_amount})
                    code.is_deleted = True
                    code.save()
                    return response
        raise NotFound('invalid code')

    def get(self, request):
        total_price = self.get_user_cart(self.request, total=True)['total_price']
        discount = CalculateDiscount.discount_amount
        shipping_price = CalculateDiscount.shipping_price
        if discount < 100:
            final_price = (total_price + shipping_price) * (1-discount/100)
            discount = (total_price + shipping_price) * (discount/100)
        else:
            final_price = (total_price + shipping_price) - (discount)
        return Response({'total_price': total_price, 'discount': discount, 'shipping_price': shipping_price, 'final_price': final_price})


class SubmitOrder(APIView, BasicViewMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_price = self.get_user_cart(self.request, total=True)['total_price']
        discount = CalculateDiscount.discount_amount
        shipping_price = CalculateDiscount.shipping_price
        if discount < 100:
            final_price = (total_price + shipping_price) * (1-discount/100)
            discount = (total_price + shipping_price) * (discount/100)
        else:
            final_price = (total_price + shipping_price) - (discount)
        return Response({'total_price': total_price, 'discount': discount, 'shipping_price': shipping_price, 'final_price': final_price})