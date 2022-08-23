from rest_framework import viewsets

from .serializers import AdvertisementSerializer, CitySerializer, CategorySerializer, ChildCategorySerializer, \
    AdsSubscriberSerializer, AdsImageSerializer, NumberSerializer, ViewStatisticSerializer
from .models import Category, ChildCategory, Advertisement, AdsSubscriber, AdsImage, City, Number, ViewStatistic


class AdvertisementAPIView(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()


class CityAPIView(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CategoryAPIView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ChildCategoryAPIView(viewsets.ModelViewSet):
    serializer_class = ChildCategorySerializer
    queryset = ChildCategory.objects.all()


class AdsSubscriberAPIView(viewsets.ModelViewSet):
    serializer_class = AdsSubscriberSerializer
    queryset = AdsSubscriber.objects.all()


class AdsImageAPIView(viewsets.ModelViewSet):
    serializer_class = AdsImageSerializer
    queryset = AdsImage.objects.all()


class NumberAPIView(viewsets.ModelViewSet):
    serializer_class = NumberSerializer
    queryset = Number.objects.all()


class ViewStatisticAPIView(viewsets.ModelViewSet):
    serializer_class = ViewStatisticSerializer
    queryset = ViewStatistic.objects.all()
