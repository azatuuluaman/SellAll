from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from advertisement.utils import Redis
from .serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from .tasks import send_ads_for_emails, send_message_to_email

User = get_user_model()


class UserAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='patch', request_body=UserUpdateSerializer)
    @action(methods=['patch'], detail=False)
    def patch(self, request):
        user = request.user
        data = request.data

        if type(data) != dict:
            data._mutable = True

        if user.is_superuser:
            id = request.data.get('id')

            if id:
                user = User.objects.get(pk=id)

        serializer = UserUpdateSerializer()
        user = serializer.update(user, data)

        return Response(user.tokens(), status=status.HTTP_202_ACCEPTED)


class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        data = request.data
        context = {'request': request}
        serializer = UserRegisterSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Пользователь успешно зарегистрирован', status=status.HTTP_201_CREATED)


class UserActivationView(views.APIView):
    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'activate_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='integer'),
        }
    ), responses=({
        status.HTTP_200_OK: "message",
        status.HTTP_400_BAD_REQUEST: 'message',
        status.HTTP_204_NO_CONTENT: 'message',
        status.HTTP_422_UNPROCESSABLE_ENTITY: 'activate_code',
    }))
    @action(methods=['POST'], detail=False)
    def post(self, request, *args, **kwargs):
        """
        Take activate_code
        """
        activate_code = request.data.get('activate_code')

        if not activate_code:
            return Response({'activate_code': 'Write activate_code!'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        redis = Redis()
        key = f'activate_code_{activate_code}'

        user_pk = redis.conn.get(key)

        if not user_pk:
            return Response({'message': 'Неправильный код активации, либо код уже не актуален!'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=user_pk.decode('utf-8'))

        if not user:
            return Response({'message': 'User not found'}, status=status.HTTP_204_NO_CONTENT)

        user.is_active = True
        user.save()

        redis.conn.delete(key)
        redis.close()

        return Response({"message": "Активация прошла успешно!"}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(views.APIView):
    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
        }))
    @action(methods=['POST'], detail=False)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'email': 'Email can\' be empty!'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        new_password = get_random_string(16)

        user.set_password(new_password)
        user.save()

        email_body = ['Пароль успешно сброшен!', f'Ваш новый пароль {new_password}']

        message = {
            'email_subject': 'Сброс пароля',
            'email_body': '\n'.join(email_body),
            'to_whom': user.email
        }

        send_message_to_email.delay(message)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class SendMassAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        send_ads_for_emails.delay()
        return Response('Sending message for all users!', status=status.HTTP_200_OK)


class UsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class DeleteUserAPIView(views.APIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(method='delete', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description='User id'),
        }))
    @action(methods=['DELETE'], detail=False)
    def delete(self, request, *args, **kwargs):
        pk = request.data.get('pk')
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({'message': 'User success deleted!'}, status=status.HTTP_200_OK)
