from django.shortcuts import render


# Create your views here.
def Example(request):
    return render(request, "landing_page_base.html")