"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from product.views import *
from user.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Home.as_view(), name="Home-page"),
    path("register/", Register.as_view(), name="Register"),
    path("verification/", Verification.as_view(), name="Verification"),
    path("login/", Login.as_view(), name="Login"),
    path("profile/", Profile.as_view(), name="Profile"),
    path("category/<int:pk>/", CategoryProducts.as_view(), name="Category-page"),
    path("product/<int:pk>/", ProductDetails.as_view(), name="Product-page"),
    path("api/v1/user/", include('user.api.v1.urls')),
    path("api/v1/cart/", include('order.api.v1.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
