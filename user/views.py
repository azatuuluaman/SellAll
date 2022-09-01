from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import User
from .serializers import UserRegisterSerializer, ActivationSerializer

User = get_user_model()


class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        data = request.data
        context = {'request': request}
        serializer = UserRegisterSerializer(data=data, context=context)
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
        return Response({"message": "Код был успешно отправлен!"}, status=status.HTTP_200_OK)

