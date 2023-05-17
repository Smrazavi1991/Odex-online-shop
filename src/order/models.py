from django.db import models
from core.models import BaseModel


# Create your models here.
class Cart(BaseModel):
    pass
    # customer
    # item
    # shipping_price


class Order(BaseModel):
    pass
    # cart
    # status


class DiscountCoupon(BaseModel):
    pass
    # code
    # discount
    # owner
