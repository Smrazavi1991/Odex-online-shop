from django.db import models
from core.models import BaseModel
from core.fields import JDateTimeField
from user.models import User

# Create your models here.
class InformationItem(BaseModel):
    name = models.CharField(max_length=100)


class Discount(BaseModel):
    types = [
        ('%', 'percentage'),
        ('$', 'non-percentage')
    ]
    type = models.CharField(choices=types, max_length=1)
    amount = models.IntegerField()
    # must have validator

class Category(BaseModel):
    name = models.CharField(max_length=100)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField('Category Is Active', default=True)
    info_item = models.ManyToManyField(InformationItem, null=True)
    sub = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    discount_activate_at = JDateTimeField('Activate at')
    discount_deactivate_at = JDateTimeField('Deactivate at')
    discount_is_active = models.BooleanField('Active discount', default=False)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    brand = models.CharField(max_length=100)
    count = models.IntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    product_info = models.JSONField()
    price = models.IntegerField()
    discount_activate_at = JDateTimeField('Activate at')
    discount_deactivate_at = JDateTimeField('Deactivate at')
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
