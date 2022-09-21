from rest_framework import generics, viewsets, permissions

from advertisement.models import ComplainingForAds, Advertisement
from advertisement.serializers import ComplainingForAdsSerializer, AdvertisementRetrieveSerializer


class AdminComplainingView(viewsets.ModelViewSet):
    queryset = ComplainingForAds.objects.all()
    serializer_class = ComplainingForAdsSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'put', 'patch', 'delete']


class AdvertisementByComplaining(generics.ListAPIView):
    queryset = Advertisement.objects.filter(complain__isnull=False)
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [permissions.IsAdminUser]
