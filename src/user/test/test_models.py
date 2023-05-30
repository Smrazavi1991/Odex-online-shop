from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from user.models import *


#######################
# Address MODEL TESTS #
#######################
class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        Address.objects.create(province='Tehran', city='Tehran', address='narmak', postal_code='1648798614')

    def test_province_label(self):
        """
        Test that label of "province" field is set right.
        """
        address = Address.objects.get(id=1)
        field_label = address._meta.get_field('province').verbose_name
        self.assertEqual(field_label, 'Province')

    def test_province_max_length(self):
        """
        Test that "province" field attribute "max_length" is set right.
        """
        address = Address.objects.get(id=1)
        max_length = address._meta.get_field('province').max_length
        self.assertEqual(max_length, 100)

    def test_province_not_nullable(self):
        """
        Test that value of "province" field "null" attribute is set to "False".
        """
        address = Address.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            address.province = None
            address.save()

    def test_province_blank(self):
        """
        Test that value of "province" field "Blank" attribute is set to "False".
        """
        address = Address.objects.get(id=1)
        with self.assertRaises(ValidationError):
            address.province = ''
            address.full_clean()

    def test_addresses_non_uniqueness(self):
        """
        Test that "Address" class objects can common.
        """
        address2 = Address.objects.create(province='Tehran', city='Tehran', address='narmak', postal_code='1648798614')
        address2.save()
        self.assertTrue(Address.objects.filter(id=2).exists())

    def test_city_label(self):
        """
        Test that label of "city" field is set right.
        """
        address = Address.objects.get(id=1)
        field_label = address._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'City')

    def test_city_max_length(self):
        """
        Test that "city" field attribute "max_length" is set right.
        """
        address = Address.objects.get(id=1)
        max_length = address._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)

    def test_city_not_nullable(self):
        """
        Test that value of "city" field "null" attribute is set to "False".
        """
        address = Address.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            address.city = None
            address.save()

    def test_city_blank(self):
        """
        Test that value of "city" field "Blank" attribute is set to "False".
        """
        address = Address.objects.get(id=1)
        with self.assertRaises(ValidationError):
            address.city = ''
            address.full_clean()

    def test_address_label(self):
        """
        Test that label of "address" field is set right.
        """
        address_obj = Address.objects.get(id=1)
        field_label = address_obj._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'Address')

    def test_address_max_length(self):
        """
        Test that "address" field attribute "max_length" is set right.
        """
        address_obj = Address.objects.get(id=1)
        max_length = address_obj._meta.get_field('address').max_length
        self.assertEqual(max_length, 2000)

    def test_address_not_nullable(self):
        """
        Test that value of "address" field "null" attribute is set to "False".
        """
        address_obj = Address.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            address_obj.address = None
            address_obj.save()

    def test_address_blank(self):
        """
        Test that value of "address" field "Blank" attribute is set to "False".
        """
        address_obj = Address.objects.get(id=1)
        with self.assertRaises(ValidationError):
            address_obj.address = ''
            address_obj.full_clean()

    def test_postal_code_label(self):
        """
        Test that label of "postal_code" field is set right.
        """
        address = Address.objects.get(id=1)
        field_label = address._meta.get_field('postal_code').verbose_name
        self.assertEqual(field_label, 'Postal Code')

    def test_postal_code_max_length(self):
        """
        Test that "postal_code" field attribute "max_length" is set right.
        """
        address = Address.objects.get(id=1)
        max_length = address._meta.get_field('postal_code').max_length
        self.assertEqual(max_length, 10)

    def test_postal_code_not_nullable(self):
        """
        Test that value of "postal_code" field "null" attribute is set to "False".
        """
        address = Address.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            address.postal_code = None
            address.save()

    def test_postal_code_blank(self):
        """
        Test that value of "postal_code" field "Blank" attribute is set to "False".
        """
        address = Address.objects.get(id=1)
        with self.assertRaises(ValidationError):
            address.postal_code = ''
            address.full_clean()

    def test_verbose_name_plural(self):
        self.assertEqual(Address._meta.verbose_name_plural, 'Addresses')


#######################
# User MODEL TESTS #
#######################
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        user = User.objects.create(username='alireza', password='123456', email='alireza@user.com', phone='09126145528')

    def test_valid_email(self):
        # Retrieve the instance from the database and assert that the email is correct
        user = User.objects.get(id=1)
        self.assertEqual(user.email, 'alireza@user.com')

    def test_invalid_email(self):
        user = User.objects.get(id=1)
        # Create an instance of MyModel with an invalid email
        with self.assertRaises(ValidationError):
            user.email = 'invalid_email'
            user.full_clean()

        # Confirm that no instances were saved to the database
        self.assertEqual(User.objects.count(), 1)

    def test_email_label(self):
        """
        Test that label of "email" field is set right.
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email Address')

    def test_email_not_nullable(self):
        """
        Test that value of "email" field "null" attribute is set to "False".
        """
        user = User.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            user.email = None
            user.save()

    def test_email_blank(self):
        """
        Test that value of "email" field "Blank" attribute is set to "False".
        """
        user = User.objects.get(id=1)
        with self.assertRaises(ValidationError):
            user.email = ''
            user.full_clean()

    def test_email_uniqueness(self):
        """
        Test that "email" field uniqueness.
        """
        with self.assertRaises(IntegrityError):
            user = User.objects.create(username='mohammad', password='1234567', email='alireza@user.com', phone='09125145528')
            user.save()

    def test_phone_label(self):
        """
        Test that label of "phone" field is set right.
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('phone').verbose_name
        self.assertEqual(field_label, 'Phone')
