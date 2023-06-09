from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from user.views import *

urlpatterns = [
    path("", Profile.as_view(), name="Profile"),
    path("user_orders-list/", UserOrdersList.as_view(), name="User orders list"),
    path("user-order-detail/<int:pk>/", UserOrderDetail.as_view(), name="User order detail"),
    path("user-order-tracking/<int:pk>/", UserOrderTracking.as_view(), name="User order tracking"),
    path("user-information/", UserInformation.as_view(), name="User information"),
    path("user-address/", UserAddress.as_view(), name="User address"),
    path("change-password/", ChangePassword.as_view(), name="Change password"),
    path("logout/", Logout.as_view(), name="Logout")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
