from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from core.models import BaseModel
from django_jalali.db import models as jmodels
from user.models import User

# Create your models here.


class InformationItem(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Discount(BaseModel):
    amount_of_percentage_discount = models.PositiveIntegerField(validators=[MaxValueValidator(80)], null=True, blank=True)
    amount_of_non_percentage_discount = models.PositiveIntegerField(null=True, blank=True)


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField('Category Is Active', default=True)
    info_item = models.ManyToManyField(InformationItem)
    sub = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    discount_activate_at = jmodels.jDateTimeField('Discount Activate at', null=True, blank=True)
    discount_deactivate_at = jmodels.jDateTimeField('Discount Deactivate at', null=True, blank=True)
    discount_is_active = models.BooleanField('Active discount', default=False)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    brand = models.CharField(max_length=100)
    count = models.PositiveIntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    product_info = models.JSONField()
    price = models.PositiveIntegerField()
    discount_activate_at = jmodels.jDateTimeField('Discount Activate at', null=True, blank=True)
    discount_deactivate_at = jmodels.jDateTimeField('Discount Deactivate at', null=True, blank=True)
    discount_is_active = models.BooleanField('Active discount', default=False)


class ProductComment(BaseModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField('Comment Approved', default=False)


class ProductImage(BaseModel):
    image = models.ImageField(upload_to='media/product_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
