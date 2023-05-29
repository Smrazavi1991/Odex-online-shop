from rest_framework.views import APIView
from rest_framework.response import Response


class ObtainToken(APIView):
    def post(self, request):
        serializer_ = OtpSerializer(request.data)
        serializer_.is_valid(raise_exeption= True)
        serializer_.save()
        return Response(serializer_.data)