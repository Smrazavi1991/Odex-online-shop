from django.db.models import Q

from product.models import Category, ProductImage


# Create your views here.
class BasicViewMixin:

    criterion1 = Q(is_deleted=False)
    criterion2 = Q(is_active=True)
    categories = Category.objects.filter(criterion1 & criterion2)
    template_name = "landing_page_base.html"

    @staticmethod
    def get_user_cart(request, total: False):
        cart = request.COOKIES.get("cart", None)
        if not cart:
            return None
        else:
            product_list = []
            total_price = 0
            temp_name_count = {}
            temp = cart.split(';')
            for product in range(len(temp)):
                products = eval(temp[product])
                products['name'] = products['name'].decode('utf-8')
                condition1 = Q(product_id=products['pk'])
                condition2 = Q(is_primary=True)
                product_image = ProductImage.objects.filter(condition1 & condition2).first()
                if product_image:
                    products['image'] = product_image
                else:
                    products['image'] = None
                total_price += int(products['price']) * products['count']
                if len(temp_name_count) == 0:
                    temp_name_count = {int(products['pk']): products['count']}
                    product_list.append(products)
                else:
                    for k, v in temp_name_count.items():
                        if int(products['pk']) == k:
                            temp_name_count[k] += 1
                            del products
                            break
                    else:
                        temp_name_count.setdefault(int(products['pk']), products['count'])
                        product_list.append(products)
            total_count = 0
            for k, v in temp_name_count.items():
                total_count += v
                for item in product_list:
                    if k == int(item['pk']):
                        item['count'] = v

            if not total:
                return product_list
            else:
                return {"total_price": total_price, 'total_count': total_count}


class ProductsViewMixin:

    @staticmethod
    def get_pics_from_a_product_queryset(queryset, is_primary=None):
        list_of_product_image = []
        for product in queryset:
            temp_dict = {}
            temp_list = []
            if not is_primary:
                product_image = ProductImage.objects.filter(product_id=product.id)
            else:
                condition1 = Q(product_id=product.id)
                condition2 = Q(is_primary=is_primary)
                product_image = ProductImage.objects.filter(condition1 & condition2).first()

            if product_image and not isinstance(product_image, ProductImage):
                temp_dict.setdefault("id", product.id)
                for obj in product_image:
                    temp_list.append(obj)
                temp_dict.setdefault("image", temp_list)
                list_of_product_image.append(temp_dict)
                continue

            if product_image:
                temp_dict.setdefault("id", product.id)
                temp_dict.setdefault("image", product_image.image)
            else:
                temp_dict.setdefault("id", product.id)
                temp_dict.setdefault("image", None)
            list_of_product_image.append(temp_dict)
        return list_of_product_image

    @staticmethod
    def get_discount_price_from_a_product_queryset(queryset):
        price_after_discount = []
        _ = 0
        for product in queryset:
            temp_dict = {}

            if product.discount:
                if product.discount.amount_of_percentage_discount:
                    _ = product.price * (product.discount.amount_of_percentage_discount / 100)
                else:
                    _ = product.discount.amount_of_non_percentage_discount

            categories = Category.objects.filter(product__id=product.id)
            for category in categories:
                if category.discount_is_active:
                    if category.discount.amount_of_percentage_discount:
                        _ += product.price_after_discount * (category.discount.amount_of_percentage_discount / 100)
                    else:
                        _ += product.discount.amount_of_non_percentage_discount
            temp_dict.setdefault("id", product.id)
            if _ == 0:
                temp_dict.setdefault("price", None)
            else:
                temp_dict.setdefault("price", product.price - _)
            price_after_discount.append(temp_dict)
        return price_after_discount

