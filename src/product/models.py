from django.db import models
from core.models import BaseModel


# Create your models here.
class Category(BaseModel):
    pass
    # name
    # discount
    # is_active
    # info_item
    # sub
    # discount_activate_at
    # discount_deactivate_at
    # discount_is_active


class InformationItem(BaseModel):
    pass
    # name


class Product(BaseModel):
    pass
    # name
    # #category
    # brand
    # count
    # discount
    # product_info
    # price
    # discount_activate_at
    # discount_deactivate_at
    # discount_is_active


class ProductComment(BaseModel):
    pass
    # title
    # description
    # product
    # owner
    # reply
    # is_approved


class ProductImage(BaseModel):
    pass
    # image
    # product


class Discount(BaseModel):
    pass
    # type
    # amount
