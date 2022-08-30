from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    AdvertisementSerializer,
    CitySerializer,
    CategorySerializer,
    ChildCategorySerializer,
    AdsSubscriberSerializer,
    AdsImageSerializer,
    NumberSerializer,
    ViewStatisticSerializer
)

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    AdsImage,
    City,
    Number,
    ViewStatistic
)


class AdvertisementPriceFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        child_category_id = request.query_params.get('child_category_id')
        price = request.query_params.get('price')
        max_price = request.query_params.get('max_price')
        has_image = request.query_params.get('has_image')
        filters = {}
        if child_category_id:
            filters['child_category'] = int(child_category_id)
        if has_image == 'True':
            filters['images__isnull'] = False
        if price:
            filters['price__gte'] = price
        if max_price:
            filters['max_price__lte'] = max_price
        queryset = queryset.filter(**filters).distinct()
        return queryset


class AdvertisementAPIView(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementPriceFilterBackend)
    filterset_fields = ('child_category', 'city', 'is_delete')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


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
