from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, status

from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    AdvertisementSerializer,
    AdvertisementListSerializer,
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

from .permissions import IsOwnerOrSuperUser


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
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementPriceFilterBackend)
    filterset_fields = ('child_category', 'city', 'is_delete')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = AdvertisementSerializer

        if self.action == 'GET':
            serializer_class = AdvertisementListSerializer

        return serializer_class

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.is_authenticated and not user.is_superuser:
            queryset = Advertisement.objects.filter(owner=user)

        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class CityAPIView(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ChildCategoryAPIView(generics.ListAPIView):
    serializer_class = ChildCategorySerializer
    queryset = ChildCategory.objects.all()


class AdsSubscriberAPIView(generics.ListAPIView):
    serializer_class = AdsSubscriberSerializer
    queryset = AdsSubscriber.objects.all()


class AdsImageAPIView(generics.ListAPIView):
    serializer_class = AdsImageSerializer
    queryset = AdsImage.objects.all()


class NumberAPIView(generics.ListAPIView):
    serializer_class = NumberSerializer
    queryset = Number.objects.all()


class ViewStatisticAPIView(generics.GenericAPIView):
    serializer_class = ViewStatisticSerializer
    queryset = ViewStatistic.objects.all()

    def get_queryset(self):
        return ViewStatistic.objects.filter(advertisement=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
