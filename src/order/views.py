from django.shortcuts import render
from django.views import View
from core.views import BasicViewMixin


# Create your views here.
class Cart(View, BasicViewMixin):
    def get(self, request):
        return render(request, "order/cart.html", {"categories": self.categories})
