from django.db.models import Q
from django.shortcuts import render
from core.views import BasicViewMixin, ProductsViewMixin
from django.views.generic import ListView
from .models import ProductImage, Product, Category
from django.views import View


# Create your views here.
class Home(ListView, BasicViewMixin, ProductsViewMixin):
    condition1 = Q(discount_is_active=True)
    condition2 = Q(discount=True)
    queryset = Product.objects.filter(condition1 & condition2)
    template_name = "product/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.category['categories']
        context["product_pictures"] = ProductsViewMixin.get_pics_from_a_product_queryset(queryset=self.queryset)
        context["discounted_price"] = ProductsViewMixin.get_discount_price_from_a_product_queryset(queryset=self.queryset)
        print(context)
        return context


class CategoryProducts(ListView, BasicViewMixin, ProductsViewMixin):
    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])
    template_name = "product/list_of_product_of_a_category.html"

    def get_category(self):
        return Category.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BasicViewMixin.queryset['categories']
        for product in self.get_queryset():
            if product in self.discount_products:
                product
        context['product_pictures'] = self.list_of_product_image
        context['discounted_price'] = self.price_after_discount
        context['category'] = self.get_category()
        print(context)
        return context

