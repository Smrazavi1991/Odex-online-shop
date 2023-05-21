import datetime

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from user.models import User
from product.models import *


###############################
# InformationItem MODEL TESTS #
###############################
class InformationItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        InformationItem.objects.create(name='Size')

    def test_name_label(self):
        """
        Test that label of "name" field is set right.
        """
        information_item = InformationItem.objects.get(id=1)
        field_label = information_item._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Name')

    def test_name_max_length(self):
        """
        Test that "name" field attribute "max_length" is set right.
        """
        information_item = InformationItem.objects.get(id=1)
        max_length = information_item._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_name_uniqueness(self):
        """
        Test that "name" field uniqueness.
        """
        with self.assertRaises(IntegrityError):
            information_item2 = InformationItem.objects.create(name='Size')
            information_item2.save()

    def test_str_method(self):
        """
        Test that object name is equal to "self.name".
        """
        information_item = InformationItem.objects.get(id=1)
        expected_object_name = information_item.name
        self.assertEqual(str(information_item), expected_object_name)


########################
# Discount MODEL TESTS #
########################
class DiscountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        Discount.objects.create(amount_of_percentage_discount=60, amount_of_non_percentage_discount=10000)

    def test_amount_of_percentage_discount_label(self):
        """
        Test that label of "amount_of_percentage_discount" field is set right.
        """
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('amount_of_percentage_discount').verbose_name
        self.assertEqual(field_label, 'Amount Of Percentage Discount')

    def test_amount_of_percentage_discount_validator(self):
        """
        Test that validator of "amount_of_percentage_discount" field work properly.
        """
        with self.assertRaises(ValidationError):
            discount = Discount.objects.create(amount_of_percentage_discount=90)
            discount.full_clean()

    def test_amount_of_percentage_discount_not_nullable(self):
        """
        Test that value of "amount_of_percentage_discount" field "null"attribute is set to "False".
        """
        discount = Discount.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            discount.is_deleted = None
            discount.save()

    # def test_is_deleted_blank(self):
    #     """
    #     Test that value of "is_deleted" field "Blank" is set to "False".
    #     """
    #     cart = Cart.objects.get(id=1)
    #     with self.assertRaises(ValidationError):
    #         cart.is_deleted = ''
    #         cart.save()
