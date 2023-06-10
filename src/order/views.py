from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from core.views import BasicViewMixin


# Create your views here.
class Cart(View, BasicViewMixin):
    def get(self, request):
        return render(request, "order/cart.html", {"categories": self.categories})


class ReviewOrder(LoginRequiredMixin, View, BasicViewMixin):
    login_url = "/login/"

    def get(self, request):
        return render(request, "order/review-order.html", {"categories": self.categories})


class OrderConfirmation(LoginRequiredMixin, View, BasicViewMixin):
    login_url = "/login/"

    def get(self, request):
        return render(request, "order/order-confirmation.html", {"categories": self.categories})