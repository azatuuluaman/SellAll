from django.contrib.auth import get_user_model

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from advertisement.utils import Redis
from .serializers import UserRegisterSerializer, UserSerializer
from .tasks import send_ads_for_emails

User = get_user_model()


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

        return Response({"message": "Активация прошла успешно!"}, status=status.HTTP_200_OK)


class UserAPIVIew(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendMassAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        send_ads_for_emails.delay()
        return Response('Sending message for all users!', status=status.HTTP_200_OK)
