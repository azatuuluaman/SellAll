from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from advertisement.models import Advertisement, Favorite
from advertisement.serializers import AdvertisementRetrieveSerializer


class FavoriteAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ Return favorites advertisement list"""
        advertisement = Advertisement.objects.prefetch_related('favorites').filter(favorites__user=request.user)
        serializer = AdvertisementRetrieveSerializer(advertisement, many=True, context={'request': request})
        return Response({'count': advertisement.count(), 'results': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'ads_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                             },
                             operation_description='Uninstall a version of Site'))
    @action(['post'], detail=False)
    def post(self, request, *args, **kwargs):
        """ Add advertisemtn to favoritest"""
        ads_id = request.data.get('ads_id')

        if not ads_id:
            return Response({"ads_id": "Can't be empty!"}, status=status.HTTP_400_BAD_REQUEST)

        ads = Advertisement.objects.prefetch_related('favorites').filter(pk=ads_id)

        if not ads.exists():
            return Response({"ads_id": "Advertisement not found!"}, status=status.HTTP_400_BAD_REQUEST)

        favorites = Favorite.objects.get_or_create(user=request.user)
        favorites[0].advertisements.add(ads[0].pk)

        return Response({"message": "Advertisement success added!"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='delete',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'ads_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                             },
                             operation_description='Uninstall a version of Site'))
    @action(['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        """ Delete advertisement from favorites"""
        ads_id = request.data.get('ads_id')

        if not ads_id:
            return Response({"advertisement_id": "Can't be empty!"}, status=status.HTTP_400_BAD_REQUEST)

        favorites = Favorite.objects.filter(advertisement_id=ads_id, user=request.user)

        if not favorites.exists():
            return Response({"favorites": "Not found!"}, status=status.HTTP_400_BAD_REQUEST)

        favorites[0].advertisements.remove(ads_id)

        return Response({"message": "Success deleted!"}, status=status.HTTP_200_OK)
