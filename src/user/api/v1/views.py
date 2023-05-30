from django.contrib.auth import login
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.authentication import JWTAuthentication
import redis

from .serializers import ObtainTokenSerializer, ObtainTokenOTPSerializer
from user.models import User
from core.utils import identify_user_role


class ObtainTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        elif identify_user_role(user.id):
            login(request, user)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        response = Response({'token': jwt_token})
        response.set_cookie("token", jwt_token)

        return response


class ObtaintTokenOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ObtainTokenOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.validated_data.get('verification_code')

        r = redis.Redis(host='localhost', port=6379, db=0)
        user_identifier = request.COOKIE.get('user_email_or_phone', None)
        storedcode = r.get(user_identifier).decode()
        if verification_code == storedcode:
            condition1 = Q(email=user_identifier)
            condition2 = Q(phone=user_identifier)
            user = User.objects.filter(condition1 | condition2).first()
            if user is None:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            elif identify_user_role(user.id):
                login(request, user)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        response = Response({'token': jwt_token})
        response.set_cookie("token", jwt_token)

        return response


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        content = {"message": "yes we can"}
        return Response(content)

