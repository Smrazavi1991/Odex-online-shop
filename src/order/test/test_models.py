from django.core.exceptions import ValidationError
from django.test import TestCase

from order.models import *
from user.models import User


class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='alireza', password='123456', email='alireza@user.com', phone='09126145528')
        Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=10000)

    def test_customer_foreign_key(self):
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.customer.username, 'alireza')

    def test_customer_foreign_key_on_delete_set_null(self):
        user = User.objects.get(username='alireza')
        user.delete()
        cart = Cart.objects.get(id=1)
        self.assertIsNone(cart.customer)

    def test_item_label(self):
        cart = Cart.objects.get(id=1)
        field_label = cart._meta.get_field('item').verbose_name
        self.assertEqual(field_label, 'Item in cart')

    def test_json_field(self):
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.item['shirt'], 2)

        cart.item['shirt'] = 5
        cart.save()

        updated_cart = Cart.objects.get(id=1)
        self.assertEqual(updated_cart.item['shirt'], 5)

    def test_shipping_price_label(self):
        cart = Cart.objects.get(id=1)
        field_label = cart._meta.get_field('shipping_price').verbose_name
        self.assertEqual(field_label, 'Shipping Price')

    def test_shipping_price_minimum_value_is_zero(self):
        user = User.objects.create(username='admin2', password='123456', email='user2@user.com', phone='09124145528')
        obj = Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=-1)
        self.assertRaises(ValidationError, obj.full_clean)


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='alireza', password='123456', email='alireza@user.com', phone='09126145528')
        cart = Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=10000)
        Order.objects.create(cart=cart, status='r')

    def test_cart_foreign_key(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.cart.shipping_price, 10000)

    def test_customer_foreign_key_on_delete_cascade(self):
        cart = Cart.objects.get(shipping_price=10000)
        cart.delete()
        self.assertFalse(Order.objects.filter(id=1).exists())

    def test_status_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Status')

    def test_status_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

    def test_choices_field(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.status, 'r')

        order.status = 'p'
        order.save()

        updated_order = Order.objects.get(id=1)
        self.assertEqual(updated_order.status, 'p')

        order.status = 's'
        order.save()

        updated_order = Order.objects.get(id=1)
        self.assertEqual(updated_order.status, 's')

        order.status = 'd'
        order.save()

        updated_order = Order.objects.get(id=1)
        self.assertEqual(updated_order.status, 'd')
