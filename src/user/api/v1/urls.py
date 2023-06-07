from django.urls import path
from user.api.v1.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('user-address/', UserAddress.as_view(), name='User address'),
    # path("obtaintoken/", ObtainToken.as_view(), name="Obtain Token"),
    # path("register/", Register.as_view(), name="Register"),
    # path("verification/", Verification.as_view(), name="Verification"),
    # path("login/", Login.as_view(), name="Login"),
    path("user-information/", UserInformation.as_view(), name="Profile-API"),
    # path("category/<int:pk>/", CategoryProducts.as_view(), name="Category-page"),
    # path("product/<int:pk>/", ProductDetails.as_view(), name="Product-page"),
    # path("api/v1/", include('user.api.v1.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
