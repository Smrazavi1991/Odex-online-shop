from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.db import models
from core.fields import JDateField
from django.core.validators import RegexValidator


# Create your models here.
class Address(BaseModel):
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=2000)
    postal_code = models.CharField(max_length=10)


class User(AbstractUser):
    genders = [
        ('m', 'male'),
        ('f', 'female')
    ]

    phone_regex = RegexValidator(regex=r'^(09)\d{9}$', message="Phone number must be entered in the format: "
                                                               "'09123456789'.")

    email = models.EmailField('email address', unique=True)
    phone = models.CharField(max_length=11, unique=True, validators=[phone_regex])
    birthday = JDateField('Birth Date', null=True, blank=True)
    gender = models.CharField(choices=genders, max_length=1, null=True, blank=True)
    profile_pic = models.ImageField(null=True, upload_to='media/user_profile_pic', blank=True)
    phone_verified = models.BooleanField('Phone Verified', default=False)
    address = models.ManyToManyField(Address, null=True, blank=True)
    is_staff = None

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
