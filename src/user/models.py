from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.db import models
from django.core.validators import RegexValidator
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Address(BaseModel):
    province = models.CharField('Province', max_length=100)
    city = models.CharField('City', max_length=100)
    address = models.CharField('Address', max_length=2000)
    postal_code = models.CharField('Postal Code', max_length=10)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.province}, {self.city}, {self.address}'


class User(AbstractUser):
    genders = [
        ('m', 'male'),
        ('f', 'female')
    ]

    phone_regex = RegexValidator(regex=r'^(09)\d{9}$', message="Phone number must be entered in the format: "
                                                               "'09123456789'.")

    email = models.EmailField('Email Address', unique=True)
    phone = models.CharField('Phone', max_length=11, unique=True, validators=[phone_regex])
    birthday = jmodels.jDateField('Birth Date', null=True, blank=True)
    gender = models.CharField('Gender', choices=genders, max_length=1, null=True, blank=True)
    profile_pic = models.ImageField('Profile Picture', null=True, upload_to='user_profile_pic', blank=True)
    phone_verified = models.BooleanField('Phone Verified', default=False)
    address = models.ManyToManyField(Address, blank=True)
    date_joined = jmodels.jDateTimeField(_("date joined"), auto_now_add=True)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()