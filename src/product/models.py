from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from core.models import BaseModel
from core.fields import JDateTimeField
from user.models import User


def max_discount_percentage(value, discount_type):
    if discount_type == '%' and value > 80:
        raise ValidationError(f"maximum percentage of discount is set to 80")


# Create your models here.
class InformationItem(BaseModel):
    name = models.CharField(max_length=100, unique=True)


class Discount(BaseModel):
    types = [
        ('%', 'percentage'),
        ('$', 'non-percentage')
    ]

    discount_type = models.CharField(choices=types, max_length=1)
    amount = models.IntegerField(validators=[max_discount_percentage])


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField('Category Is Active', default=True)
    info_item = models.ManyToManyField(InformationItem, null=True, blank=True)
    sub = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    discount_activate_at = JDateTimeField('Activate at', null=True, blank=True)
    discount_deactivate_at = JDateTimeField('Deactivate at', null=True, blank=True)
    discount_is_active = models.BooleanField('Active discount', default=False)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    brand = models.CharField(max_length=100)
    count = models.IntegerField(validators=[MinValueValidator(0)])
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    product_info = models.JSONField()
    price = models.IntegerField(validators=[MinValueValidator(0)])
    discount_activate_at = JDateTimeField('Activate at', null=True, blank=True)
    discount_deactivate_at = JDateTimeField('Deactivate at', null=True, blank=True)
    discount_is_active = models.BooleanField('Active discount', default=False)


class ProductComment(BaseModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="Anonymous")
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField('Comment Approved', default=False)


class ProductImage(BaseModel):
    image = models.ImageField(upload_to='media/product_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
