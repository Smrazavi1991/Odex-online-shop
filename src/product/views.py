from django.db.models import Q
from core.views import BasicViewMixin, ProductsViewMixin
from django.views.generic import ListView
from .models import Product, Category


# Create your views here.
class Home(ListView, BasicViewMixin, ProductsViewMixin):
    condition1 = Q(discount_is_active=True)
    condition2 = Q(discount=True)
    queryset = Product.objects.filter(condition1 & condition2)
    template_name = "product/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.category['categories']
        context["product_pictures"] = self.get_pics_from_a_product_queryset(queryset=self.queryset)
        context["discounted_price"] = self.get_discount_price_from_a_product_queryset(queryset=self.queryset)
        return context


class CategoryProducts(ListView, BasicViewMixin, ProductsViewMixin):
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])
    template_name = "product/list_of_product_of_a_category.html"

    def get_category(self):
        return Category.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = self.category['categories']
        context['product_pictures'] = self.get_pics_from_a_product_queryset(queryset=self.get_queryset())
        context['discounted_price'] = self.get_discount_price_from_a_product_queryset(queryset=self.get_queryset())
        context['category'] = self.get_category()
        print(context)
        return context

