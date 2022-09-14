import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({'message': "Нельзя войти через эту учетную запись!"}, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({'message': "Нельзя войти через эту учетную запись!"}, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)

