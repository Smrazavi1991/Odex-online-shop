from django.core.validators import MinValueValidator
from django.db import models
from core.models import BaseModel
from user.models import User
from product.models import Discount


# Create your models here.
class Cart(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='Anonymous')
    item = models.JSONField()
    shipping_price = models.IntegerField(validators=[MinValueValidator(0)])


class Order(BaseModel):
    statuses = [
        ('r', 'registered'),
        ('p', 'processing'),
        ('s', 'sent'),
        ('d', 'delivered')
    ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(choices=statuses, max_length=1)


class DiscountCoupon(BaseModel):
    code = models.CharField(max_length=10)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
