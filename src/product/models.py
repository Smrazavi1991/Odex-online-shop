from django.core.validators import MaxValueValidator
from django.db import models
from core.models import BaseModel
from django_jalali.db import models as jmodels
from user.models import User
import jdatetime
from django.utils.html import mark_safe

# Create your models here.


class InformationItem(BaseModel):
    name = models.CharField('Name', max_length=100, unique=True)

    def __str__(self):
        return self.name


class Discount(BaseModel):
    amount_of_percentage_discount = models.PositiveIntegerField('Amount Of Percentage Discount', validators=[MaxValueValidator(80)], null=True, blank=True, unique=True)
    amount_of_non_percentage_discount = models.PositiveIntegerField('Amount Of NON-Percentage Discount', null=True, blank=True, unique=True)

    def __str__(self):
        if self.amount_of_percentage_discount is None:
            return f"{self.amount_of_non_percentage_discount} Rials"
        if self.amount_of_non_percentage_discount is None:
            return f"{self.amount_of_percentage_discount} %"


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField('Category Is Active', default=True)
    info_item = models.ManyToManyField(InformationItem, blank=True)
    sub = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    discount_activate_at = jmodels.jDateTimeField('Discount Activate at', null=True, blank=True)
    discount_deactivate_at = jmodels.jDateTimeField('Discount Deactivate at', null=True, blank=True)
    discount_is_active = models.BooleanField('Active discount', default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.discount_activate_at is not None:
            if self.discount_deactivate_at is None:
                self.discount_deactivate_at = jdatetime.datetime.fromgregorian(year=2111, month=3, day=21)
        return super().save()

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

    # @staticmethod
    def img_preview(self):
        thumbnail_image = ProductImage.objects.filter(product_id=self.id).first()
        return mark_safe(f'<img src = "{thumbnail_image.image.url}" width = "100"/>')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.discount_activate_at is not None:
            if self.discount_deactivate_at is None:
                self.discount_deactivate_at = jdatetime.datetime.fromgregorian(year=2111, month=3, day=21)
        return super().save()

    def __str__(self):
        return self.name


class ProductComment(BaseModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField('Comment Approved', default=False)


class ProductImage(BaseModel):
    image = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" width = "100"/>')

    def product_name(self):
        return self.product.name

    def __str__(self):
        return f"{self.product.name} picture"

