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

    def test_name_not_nullable(self):
        """
        Test that value of "name" field "null" attribute is set to "False".
        """
        information_item = InformationItem.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            information_item.name = None
            information_item.save()

    def test_name_blank(self):
        """
        Test that value of "name" field "Blank" attribute is set to "False".
        """
        information_item = InformationItem.objects.get(id=1)
        with self.assertRaises(ValidationError):
            information_item.name = ''
            information_item.full_clean()


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
        discount = Discount.objects.get(id=1)
        discount.amount_of_percentage_discount = 80
        discount.save()
        self.assertEqual(discount.amount_of_percentage_discount, 80)
        with self.assertRaises(ValidationError):
            discount = Discount.objects.create(amount_of_percentage_discount=81)
            discount.full_clean()

    def test_amount_of_percentage_discount_null(self):
        """
        Test that value of "amount_of_percentage_discount" field "null"attribute is set to "True".
        """
        discount = Discount.objects.get(id=1)
        discount.amount_of_percentage_discount = None
        discount.save()
        self.assertIsNone(discount.amount_of_percentage_discount)

    def test_amount_of_percentage_discount_integer(self):
        """
        Test that value of "amount_of_percentage_discount" field  is just integer.
        """
        discount = Discount.objects.get(id=1)
        discount.amount_of_percentage_discount = 50
        discount.save()
        self.assertEqual(discount.amount_of_percentage_discount, 50)
        with self.assertRaises(ValueError):
            discount.amount_of_percentage_discount = "test"
            discount.save()

    def test_amount_of_percentage_discount_uniqueness(self):
        """
        Test that "amount_of_percentage_discount" field uniqueness.
        """
        with self.assertRaises(IntegrityError):
            discount2 = Discount.objects.create(amount_of_percentage_discount=60)
            discount2.save()

