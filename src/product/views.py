from django.shortcuts import render
from core.views import BasicViewMixin
from django.views.generic import ListView
from .models import ProductImage, Product
from django.views import View


# Create your views here.
class Home(View, BasicViewMixin):
    list_of_product_image = []
    discount_products = Product.objects.filter(discount_is_active=True)
    for product in discount_products:
        product_image = ProductImage.objects.filter(product_id=product.id).first()
        list_of_product_image.append(product_image)

    def get(self, request):
        self.template_name = "product/home_page.html"
        self.queryset.setdefault("discount_products", self.discount_products)
        self.queryset.setdefault("product_pictures", self.list_of_product_image)
        return super().get(request)


class CategoryProducts(ListView):
    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])
    template_name = "landing_page_base.html"


