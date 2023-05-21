import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from order.models import *
from user.models import User
from product.models import Discount


####################
# Cart MODEL TESTS #
####################
class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        user = User.objects.create(username='alireza', password='123456', email='alireza@user.com', phone='09126145528')
        Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=10000)

    def test_customer_foreign_key(self):
        """
        Test that customer that is a foreign key field work correctly.
        """
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.customer.username, 'alireza')

    def test_customer_foreign_key_attr(self):
        """
        Test that customer "on_delete" attribute that is set to "SET_NULL" work correctly.
        """
        user = User.objects.get(username='alireza')
        user.delete()
        cart = Cart.objects.get(id=1)
        self.assertIsNone(cart.customer)

    def test_customer_nullable(self):
        """
        Test that value of "customer" field "null" attribute is set to "True".
        """
        cart = Cart.objects.get(id=1)
        cart.customer = None
        cart.save()
        self.assertIsNone(cart.customer, None)

    def test_customer_blank(self):
        """
        Test that value of "customer" field "Blank" is set to "False".
        """
        cart = Cart.objects.get(id=1)
        with self.assertRaises(ValueError):
            cart.customer = ''
            cart.save()

    def test_cart_non_uniqueness(self):
        """
        Test that "Cart" class objects can common.
        """
        user = User.objects.get(username='alireza')
        cart2 = Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=10000)
        cart2.save()
        self.assertTrue(Cart.objects.filter(id=2).exists())

    def test_item_label(self):
        """
        Test that label of "item" field is set right.
        """
        cart = Cart.objects.get(id=1)
        field_label = cart._meta.get_field('item').verbose_name
        self.assertEqual(field_label, 'Item in cart')

    def test_json_field(self):
        """
        Test that "item" field (that is a Json field) is set and work correctly.
        """
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.item['shirt'], 2)

        cart.item['shirt'] = 5
        cart.save()

        updated_cart = Cart.objects.get(id=1)
        self.assertEqual(updated_cart.item['shirt'], 5)

    def test_item_not_nullable(self):
        """
        Test that value of "item" field "null" attribute is set to "False".
        """
        cart = Cart.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            cart.item = None
            cart.save()

    def test_item_blank(self):
        """
        Test that value of "item" field "Blank" is set to "False".
        """
        cart = Cart.objects.get(id=1)
        with self.assertRaises(ValidationError):
            cart.item = ''
            cart.full_clean()

    def test_shipping_price_label(self):
        """
        Test that label of "shipping_price" field is set right.
        """
        cart = Cart.objects.get(id=1)
        field_label = cart._meta.get_field('shipping_price').verbose_name
        self.assertEqual(field_label, 'Shipping Price')

    def test_shipping_price_with_negative_value(self):
        """
        Test that the positive integer field cannot have a negative value.
        """
        with self.assertRaises(IntegrityError):
            user = User.objects.create(username='admin2', password='123456', email='user2@user.com',
                                       phone='09124145528')
            cart = Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=-1)
            cart.save()

    def test_is_deleted_label(self):
        """
        Test that label of "is_deleted" field is set right.
        """
        cart = Cart.objects.get(id=1)
        field_label = cart._meta.get_field('is_deleted').verbose_name
        self.assertEqual(field_label, 'Is Deleted')

    def test_is_deleted_False(self):
        """
        Test that default value of "is_deleted" field is set to "False".
        """
        cart = Cart.objects.get(id=1)
        self.assertFalse(cart.is_deleted)

    def test_is_deleted_not_nullable(self):
        """
        Test that value of "is_deleted" field "null" attribute is set to "False".
        """
        cart = Cart.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            cart.is_deleted = None
            cart.save()

    def test_is_deleted_blank(self):
        """
        Test that value of "is_deleted" field "Blank" is set to "False".
        """
        cart = Cart.objects.get(id=1)
        with self.assertRaises(ValidationError):
            cart.is_deleted = ''
            cart.save()

    def test_function_create_delete_datetime(self):
        """
        Test that "create_delete_datetime" function works correctly.
        """
        cart = Cart.objects.get(id=1)
        cart.is_deleted = True
        cart.create_delete_datetime()
        sample_time = datetime.datetime.now().replace(microsecond=0)
        self.assertEqual(cart.delete_datetime, sample_time)

    def test_create_date_default(self):
        """
        Test that "create_date" field filled automatically when new instance created.
        """
        cart = Cart.objects.get(id=1)
        self.assertIsNotNone(cart.create_date)

    def test_create_date_and_last_change_set_nearly_equal_when_new_instance_created(self):
        """
        Test that "create_date" and "last_change" fields filled nearly equal automatically when new instance created.
        """
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.create_date.replace(microsecond=0), cart.last_change.replace(microsecond=0))

    def test_delete_datetime_nullable(self):
        """
        Test that value of "delete_datetime" field "null" attribute is set to "True".
        """
        cart = Cart.objects.get(id=1)
        cart.delete_datetime = None
        cart.save()
        self.assertIsNone(cart.delete_datetime, None)

    def test_delete_datetime_blank(self):
        """
        Test that value of "delete_datetime" field "Blank" is set to "True".
        """
        cart = Cart.objects.get(id=1)
        cart.delete_datetime = ''
        cart.save()
        self.assertEqual(cart.delete_datetime, '')


#####################
# Order MODEL TESTS #
#####################
class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        user = User.objects.create(username='alireza', password='123456', email='alireza@user.com', phone='09126145528')
        cart = Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=10000)
        Order.objects.create(cart=cart, status='r')

    def test_cart_foreign_key(self):
        """
        Test that cart that is a foreign key field work correctly.
        """
        order = Order.objects.get(id=1)
        self.assertEqual(order.cart.shipping_price, 10000)

    def test_cart_foreign_key_attr(self):
        """
        Test that customer "on_delete" attribute that is set to "Cascade" work correctly.
        """
        cart = Cart.objects.get(shipping_price=10000)
        cart.delete()
        self.assertFalse(Order.objects.filter(id=1).exists())

    def test_cart_not_nullable(self):
        """
        Test that value of "cart" field "null" attribute is set to "False".
        """
        order = Order.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            order.cart = None
            order.save()

    def test_cart_blank(self):
        """
        Test that value of "cart" field "Blank" is set to "False".
        """
        order = Order.objects.get(id=1)
        with self.assertRaises(ValueError):
            order.cart = ''
            order.save()

    def test_cart_uniqueness(self):
        """
        Test that "cart" field uniqueness.
        """
        cart = Cart.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            order2 = Order.objects.create(cart=cart, status='d')
            order2.save()


    def test_status_label(self):
        """
        Test that label of "status" field is set right.
        """
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Status')

    def test_status_max_length(self):
        """
        Test that "status" field attribute "max_length" is set right.
        """
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

    def test_choices_field(self):
        """
        Test that attribute "choices" of "status" field works correctly.
        """
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

        with self.assertRaises(ValidationError):
            order.status = 'z'
            order.full_clean()

    def test_status_not_nullable(self):
        """
        Test that value of "status" field "null" attribute is set to "False".
        """
        order = Order.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            order.status = None
            order.save()

    def test_status_blank(self):
        """
        Test that value of "status" field "Blank" is set to "False".
        """
        order = Order.objects.get(id=1)
        with self.assertRaises(ValidationError):
            order.status = ''
            order.full_clean()

    def test_status_non_uniqueness(self):
        """
        Test that "status" field can common.
        """
        user = User.objects.get(username='alireza')
        cart2 = Cart.objects.create(customer=user, item={"shirt": 2}, shipping_price=10000)
        cart2.save()
        order2 = Order.objects.create(cart=cart2, status='r')
        order2.save()
        self.assertTrue(Order.objects.filter(id=2).exists())


##############################
# DiscountCoupon MODEL TESTS #
##############################
class DiscountCouponModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        user = User.objects.create(username='alireza', password='123456', email='alireza@user.com', phone='09126145528')
        discount = Discount.objects.create(amount_of_non_percentage_discount=10000)
        x = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        DiscountCoupon.objects.create(code="abcd", discount=discount, owner=user, discount_activate_at=x)

    def test_code_label(self):
        """
        Test that label of "code" field is set right.
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        field_label = discount_coupon._meta.get_field('code').verbose_name
        self.assertEqual(field_label, 'Discount Code')

    def test_code_max_length(self):
        """
        Test that "code" field attribute "max_length" is set right.
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        max_length = discount_coupon._meta.get_field('code').max_length
        self.assertEqual(max_length, 10)

    def test_code_not_nullable(self):
        """
        Test that value of "code" field "null" attribute is set to "False".
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            discount_coupon.code = None
            discount_coupon.save()

    def test_code_blank(self):
        """
        Test that value of "code" field "Blank" is set to "False".
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        with self.assertRaises(ValidationError):
            discount_coupon.code = ''
            discount_coupon.full_clean()

    def test_code_discount_owner_non_uniqueness(self):
        """
        Test that "code, discount and owner" fields can common.
        """
        user = User.objects.get(username='alireza')
        discount = Discount.objects.get(id=1)
        discountcoupon2 = DiscountCoupon(code="abcd", discount=discount, owner=user, discount_activate_at=jdatetime.datetime.fromgregorian(year=2024, month=3, day=20, hour=20, minute=30).replace(tzinfo=datetime.timezone.utc))
        discountcoupon2.save()
        self.assertTrue(DiscountCoupon.objects.filter(id=2).exists())

    def test_discount_foreign_key(self):
        """
        Test that discount that is a foreign key field work correctly.
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        self.assertEqual(discount_coupon.discount.amount_of_non_percentage_discount, 10000)

    def test_discount_foreign_key_attr(self):
        """
        Test that discount "on_delete" attribute that is set to "Cascade" work correctly.
        """
        discount = Discount.objects.get(amount_of_non_percentage_discount=10000)
        discount.delete()
        self.assertFalse(DiscountCoupon.objects.filter(id=1).exists())

    def test_discount_not_nullable(self):
        """
        Test that value of "discount" field "null" attribute is set to "False".
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            discount_coupon.discount = None
            discount_coupon.save()

    def test_discount_blank(self):
        """
        Test that value of "discount" field "Blank" attribute is set to "False".
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        with self.assertRaises(ValueError):
            discount_coupon.discount = ''
            discount_coupon.save()

    def test_owner_foreign_key(self):
        """
        Test that owner that is a foreign key field work correctly.
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        self.assertEqual(discount_coupon.owner.username, 'alireza')

    def test_cart_foreign_key_attr(self):
        """
        Test that owner "on_delete" attribute that is set to "Cascade" work correctly.
        """
        user = User.objects.get(username='alireza')
        user.delete()
        self.assertFalse(DiscountCoupon.objects.filter(id=1).exists())

    def test_owner_not_nullable(self):
        """
        Test that value of "owner" field "null" attribute is set to "False".
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            discount_coupon.owner = None
            discount_coupon.save()

    def test_owner_blank(self):
        """
        Test that value of "owner" field "Blank" attribute is set to "False".
        """
        discount_coupon = DiscountCoupon.objects.get(id=1)
        with self.assertRaises(ValueError):
            discount_coupon.owner = ''
            discount_coupon.save()
