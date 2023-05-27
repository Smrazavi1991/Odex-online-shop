from django.db.models import Q
from product.models import Category, ProductImage


# Create your views here.
class BasicViewMixin:

    criterion1 = Q(is_deleted=False)
    criterion2 = Q(is_active=True)
    categories = Category.objects.filter(criterion1 & criterion2)
    category = {"categories": categories}
    template_name = "landing_page_base.html"


class ProductsViewMixin:

    @staticmethod
    def get_pics_from_a_product_queryset(queryset: list):
        list_of_product_image = []
        for product in queryset:
            product_image = ProductImage.objects.filter(product_id=product.id).first()
            list_of_product_image.append(product_image)
        return list_of_product_image

    @staticmethod
    def get_discount_price_from_a_product_queryset(queryset: list):
        price_after_discount = []
        for product in queryset:
            temp_dict = {}

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
        return price_after_discount
