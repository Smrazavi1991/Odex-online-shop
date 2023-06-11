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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from product.views import *
from user.views import *
from order.views import *
from user import urls

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


loginpatterns = [
    path("", Login.as_view(), name="Login"),
    path("otp-login/", OtpLogin.as_view(), name="OTP Login"),
    path("otp-verification/", Verification.as_view(), name="Verification"),
]

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("", Home.as_view(), name="Home-page"),
    path("register/", Register.as_view(), name="Register"),
    path("login/", include(loginpatterns)),
    path("profile/", include(urls)),
    path("cart", Cart.as_view(), name="Cart"),
    path("contact-us", ContactUs.as_view(), name="Contact us"),
    path("about-us", AboutUs.as_view(), name="About us"),
    path("faq", Faq.as_view(), name="Faq"),
    path("review-order/", ReviewOrder.as_view(), name="Review Order"),
    path("order-confirmation/", OrderConfirmation.as_view(), name="Order Confirmation"),
    path("category/<int:pk>/", CategoryProducts.as_view(), name="Category-page"),
    path("product/<int:pk>/", ProductDetails.as_view(), name="Product-page"),
    path("api/v1/user/", include('user.api.v1.urls')),
    path("api/v1/cart/", include('order.api.v1.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
