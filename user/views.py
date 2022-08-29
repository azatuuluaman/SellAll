from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserRegisterSerializer, ForgotPasswordSerializer, ActivationSerializer
from .utils import send_password_with_email

User = get_user_model()


class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Пользователь успешно зарегистрирован', status=201)


class ActivationView(APIView):
    # Исправить этот класс на generic create api view

    def get(self, request, code):
        serializer = ActivationSerializer(data={'activation_code': code})
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(activation_code=serializer.data['activation_code'])
        user.is_active = True
        user.save()
        return Response({"GOTOVO": "DETKA"})


class ForgotPasswordView(generics.UpdateAPIView):
    """
    an endpoint forgot password
    """
    serializer_class = ForgotPasswordSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        user = User.objects.get(email=email)
        send_password_with_email(user)

        return Response({'forgot_password': 'successfully'}, status=status.HTTP_200_OK)
