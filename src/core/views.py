from django.db.models import Q
from django.shortcuts import render
from django.views import View
from product.models import Category


# Create your views here.
class BasicViewMixin:

    criterion1 = Q(is_deleted=False)
    criterion2 = Q(is_active=True)
    categories = Category.objects.filter(criterion1 & criterion2)
    queryset = {"categories": categories}
    template_name = "landing_page_base.html"

    def get(self, request):
        return render(request, self.template_name, self.queryset)
