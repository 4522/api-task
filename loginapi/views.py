from django.http.response import JsonResponse
from loginapi.models import Profile
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from .serializers import ProfileSerializer, UserSerializer, RegisterSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ProfileAPI(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    model_class = Profile

    def get(self, request):
        data = self.model_class.objects.all()
        serializer = self.serializer_class(data, many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response("data not found")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)
