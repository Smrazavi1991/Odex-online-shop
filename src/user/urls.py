from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user.views import *

urlpatterns = [
    path("", Profile.as_view(), name="Profile"),
    path("orders-list/", OrdersList.as_view(), name="Orders list"),
    path("order-detail/<int:pk>/", OrderDetail.as_view(), name="Order detail"),
    path("order-tracking/", OrderTracking.as_view(), name="Order tracking"),
    path("user-information/", UserInformation.as_view(), name="User information"),
    path("user-address/", UserAddress.as_view(), name="User address"),
    path("change-password/", ChangePassword.as_view(), name="Change password"),
    path("logout/", Logout.as_view(), name="Logout")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
