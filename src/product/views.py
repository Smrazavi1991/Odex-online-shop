from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Category


# Create your views here.
class Home(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "landing_page_base.html", {"categories": categories})


class CategoryProducts(ListView):
    def get(self, request, pk):
        # model =
        return render(request, "landing_page_base.html")

