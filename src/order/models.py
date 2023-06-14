import datetime

from django.core.validators import MinValueValidator
from django.db import models
from core.models import BaseModel
from user.models import User, Address
from product.models import Discount
from django_jalali.db import models as jmodels
import jdatetime


# Create your models here.
class Cart(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.JSONField("Item in cart")
    shipping_price = models.CharField("Shipping Price", default="0", max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_price = models.CharField("Total Price", default="0", max_length=100)

    def customer_name(self):
        return self.customer.get_full_name()


class Order(BaseModel):
    statuses = [
        ('ثبت شده', 'ثبت شده'),
        ('در حال پردازش', 'در حال پردازش'),
        ('آماده ارسال', 'آماده ارسال')
    ]
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
    status = models.CharField('Status', choices=statuses, max_length=13)


class DiscountCoupon(BaseModel):
    code = models.CharField('Discount Code', max_length=10)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_activate_at = jmodels.jDateTimeField('Discount Activate at')
    discount_deactivate_at = jmodels.jDateTimeField('Discount Deactivate at', default=jdatetime.datetime.fromgregorian(year=2111, month=3, day=20, hour=20, minute=30).replace(tzinfo=datetime.timezone.utc))
    discount_is_active = models.BooleanField('Active discount', default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'discount', 'owner', 'discount_activate_at'], name='unique_Coupon')
        ]

    def customer_name(self):
        return self.owner.get_full_name()
