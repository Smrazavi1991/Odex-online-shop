from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.views import BasicViewMixin


# Create your views here.
class Cart(View, BasicViewMixin):
    def get(self, request):
        return render(request, "order/cart.html", {"categories": self.categories})


class ReviewOrder(View, BasicViewMixin):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request):
        return render(request, "order/review-order.html", {"categories": self.categories})
