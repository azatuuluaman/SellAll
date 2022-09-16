from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

from rest_framework import generics, status, views
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from advertisement.swagger_scheme import (
    category_id_query,
    has_image_query,
    price_query,
    max_price_query,
    limit_query,
    child_category_id_query,
    cities_query,
)

from advertisement.permissions import IsOwnerOrSuperUser

from advertisement.serializers import (
    AdvertisementSerializer,
    AdvertisementRetrieveSerializer,
    ComplainingForAdsSerializer
)

from advertisement.models import (
    Category,
    ChildCategory,
    Advertisement,
    ComplainingForAds
)
from advertisement.utils import Redis, get_client_ip


class AdvertisementCustomFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        category_id = request.query_params.get('category_id')
        price = request.query_params.get('price')
        max_price = request.query_params.get('max_price')
        has_image = request.query_params.get('has_image')
        cities = request.query_params.get('cities')

        filters = {}

        if category_id:
            filters['child_category__category_id'] = category_id

        if has_image == 'true':
            filters['images__isnull'] = False

        if cities:
            filters['city__in'] = cities.split(',')

        if price and max_price:
            min_price_filter = Q(price__gte=price)
            max_price_filter = Q(price__lte=max_price)
            queryset_1 = queryset.filter(min_price_filter & max_price_filter, **filters)
            queryset_2 = queryset_1.filter(max_price__lte=max_price, max_price__isnull=False)
            queryset = queryset_1 | queryset_2
            return queryset.distinct()
        else:
            if price:
                filters['price__gte'] = price

            if max_price:
                min_price = Q(price__lte=max_price)
                max_price = Q(max_price__lte=max_price)

                queryset = queryset.filter(min_price | max_price).filter(**filters).distinct()
                return queryset

        queryset = queryset.filter(**filters).distinct()

        return queryset


class AdvertisementCreateView(generics.CreateAPIView):
    serializer_class = AdvertisementSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        images = request.FILES.getlist('images')
        data = request.data

        context_data = {
            'images': images,
            'owner': request.user
        }

        serializer = self.get_serializer(data=data, context=context_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdvertisementRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        redis = Redis()
        ads_id = instance.pk
        date = timezone.now().date().strftime('%d.%m.%Y')
        client_ip = get_client_ip(request)

        redis.add_views(ads_id, date, client_ip)

        serializer = self.get_serializer(instance, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementListView(generics.ListAPIView):
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementCustomFilterBackend)
    filterset_fields = ('child_category_id', 'disable_date')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    @swagger_auto_schema(method='get', manual_parameters=[
        category_id_query, has_image_query, price_query, max_price_query, cities_query
    ])
    @action(['get'], detail=False)
    def get(self, request, *args, **kwargs):
        return super(AdvertisementListView, self).get(request)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(type=settings.ACTIVE)
        return queryset


class UserAdvertisementListView(generics.ListAPIView):
    """You can filter by Активный - На проверке - Неактивный. And search by name!"""
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('type',)
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(owner=self.request.user)
        return queryset


class SimularAdsView(views.APIView):
    @swagger_auto_schema(method='get', manual_parameters=[limit_query, child_category_id_query])
    @action(methods=['GET'], detail=False)
    def get(self, request, *args, **kwargs):
        """Get child category id"""

        child_category_id = self.kwargs['child_category_id']
        limit = self.request.query_params.get('limit')

        if limit:
            limit = int(limit)
        else:
            limit = 5

        child_category = get_object_or_404(ChildCategory, pk=child_category_id)

        advertisement = Advertisement.objects.filter(child_category=child_category)[:limit]
        ads_count = advertisement.count()

        if ads_count < limit:
            category = Category.objects.get(child_categories=child_category)
            simular_child_categories = ChildCategory.objects.filter(category=category.pk)

            not_enough = limit - ads_count

            for i in range(not_enough):
                not_enough = limit - ads_count
                advertisement_by_category = Advertisement.objects.filter(
                    child_category=simular_child_categories[i])[:not_enough]

                if limit >= ads_count:
                    advertisement = advertisement | advertisement_by_category
                    advertisement = advertisement.distinct()
                    break

                ads_count += len(advertisement_by_category)

        serializer = AdvertisementRetrieveSerializer(advertisement, many=True, context={'request': request})
        return Response({'count': advertisement.count(), 'results': serializer.data}, status=status.HTTP_200_OK)


class ComplainingForAdsView(generics.CreateAPIView):
    queryset = ComplainingForAds.objects.all()
    serializer_class = ComplainingForAdsSerializer
    permission_classes = [IsAuthenticated]
