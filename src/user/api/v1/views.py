from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.authentication import JWTAuthentication
import datetime

from .serializers import UserInformationSerializer



class ObtainTokenView(APIView):

    @method_decorator(login_required)
    def get(self, request):
        user = self.request.user

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        response = Response({'token': jwt_token})
        expires = datetime.datetime.now() + datetime.timedelta(weeks=999)
        expires_string = expires.strftime("%a, %d-%b-%Y %H:%M:%S")
        response.set_cookie("token", jwt_token, expires=expires_string)

        return response


class UserInformation(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInformationSerializer

    def get(self, request):
        user = self.request.user
        serializer_ = self.serializer_class(user)
        return Response(serializer_.data)

    def patch(self, request):
        user = self.request.user
        serializer_ = self.serializer_class(user, data=request.data, partial=True)
        serializer_.is_valid(raise_exception=True)
        serializer_.save()
        return Response(serializer_.data)


class UserAddress(APIView):
    pass


class ChangePassword(APIView):
    pass
