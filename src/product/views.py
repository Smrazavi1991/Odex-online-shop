from django.db.models import Q
from django.shortcuts import render
from core.views import BasicViewMixin
from django.views.generic import ListView
from .models import ProductImage, Product, Category
from django.views import View


# Create your views here.
class Home(View, BasicViewMixin):
    list_of_product_image = []
    price_after_discount = []
    condition1 = Q(discount_is_active=True)
    condition2 = Q(discount=True)
    discount_products = Product.objects.filter(condition1 & condition2)

    for product in discount_products:
        temp_dict = {}
        product_image = ProductImage.objects.filter(product_id=product.id).first()
        list_of_product_image.append(product_image)

        if product.discount.amount_of_percentage_discount:
            _ = product.price * (1 - product.discount.amount_of_percentage_discount / 100)
        else:
            _ = product.price - product.discount.amount_of_non_percentage_discount

        categories = Category.objects.filter(product__id=product.id)
        for category in categories:
            if category.discount_is_active:
                if category.discount.amount_of_percentage_discount:
                    _ = product.price_after_discount * (1 - category.discount.amount_of_percentage_discount / 100)
                else:
                    _ = product.price_after_discount - product.discount.amount_of_non_percentage_discount
        temp_dict.setdefault("id", product.id)
        temp_dict.setdefault("price", _)
        price_after_discount.append(temp_dict)


    def get(self, request):
        self.template_name = "product/home_page.html"
        self.queryset.setdefault("discount_products", self.discount_products)
        self.queryset.setdefault("product_pictures", self.list_of_product_image)
        self.queryset.setdefault("discounted_price", self.price_after_discount)
        return super().get(request)


class CategoryProducts(ListView):
    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])
    template_name = "landing_page_base.html"


