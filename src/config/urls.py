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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from product.views import *
from user.views import *
from order.views import *
from user import urls


loginpatterns = [
    path("", Login.as_view(), name="Login"),
    path("otp-login/", OtpLogin.as_view(), name="OTP Login"),
    path("otp-verification/", Verification.as_view(), name="Verification"),
]

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.
                                                                             MEDIA_ROOT)
