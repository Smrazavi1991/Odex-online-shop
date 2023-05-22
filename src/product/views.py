from django.shortcuts import render
from django.views import View
from django.views.generic import ListView


# Create your views here.
class Home(View):
    def get(self, request):

        return render(request, "landing_page_base.html")

class Category(ListView):
    def get(self, request):
        return render(request, "landing_page_base.html")

