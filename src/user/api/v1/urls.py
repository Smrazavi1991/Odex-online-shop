from django.urls import path
from user.api.v1.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('user-address/', UserAddress.as_view(), name='User address'),
    path('user-address/<int:pk>/', RemoveAddress.as_view(), name='Remove address'),
    path("user-orders-list/", UserOrdersList.as_view(), name="Orders List"),
    path("user-order-detail/<int:pk>/", UserOrderDetail.as_view(), name="User order detail"),
    path("user-order-pics/<int:pk>/", UserOrderPics.as_view(), name="User order pics"),
    path("change-password/", ChangePassword.as_view(), name="Change password"),
    path("user-information/", UserInformation.as_view(), name="Profile-API"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
