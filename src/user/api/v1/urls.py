from django.urls import path, include
from user.api.v1.views import *

urlpatterns = [
    path("obtaintoken/", ObtainToken.as_view(), name="Obtain Token"),
    # path("register/", Register.as_view(), name="Register"),
    # path("verification/", Verification.as_view(), name="Verification"),
    # path("login/", Login.as_view(), name="Login"),
    # path("profile/", Profile.as_view(), name="Profile"),
    # path("category/<int:pk>/", CategoryProducts.as_view(), name="Category-page"),
    # path("product/<int:pk>/", ProductDetails.as_view(), name="Product-page"),
    # path("api/v1/", include('user.api.v1.urls'))
]
