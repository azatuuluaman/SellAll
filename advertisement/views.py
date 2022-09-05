from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsOwnerOrSuperUser
from .serializers import (
    AdvertisementSerializer,
    AdvertisementListSerializer,
    CitySerializer,
    CategorySerializer,
    ChildCategorySerializer,
    AdsSubscriberSerializer,
    ViewStatisticSerializer
)

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    City,
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
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = (AllowAny, )

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementPriceFilterBackend)
    filterset_fields = ('child_category', 'city', 'is_delete')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = AdvertisementSerializer

        if self.action == 'list':
            serializer_class = AdvertisementListSerializer

        if self.action == 'retrieve':
            serializer_class = AdvertisementListSerializer

        return serializer_class

    def get_permissions(self):
        owner_actions = ('create', 'destroy', 'update')

        if self.action in owner_actions:
            self.permission_classes = [IsOwnerOrSuperUser]

        return super(AdvertisementAPIView, self).get_permissions()

    def get_queryset(self):
        queryset = super(AdvertisementAPIView, self).get_queryset()

        if self.action == 'list':
            return queryset

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        client_ip = get_client_ip(self.request)
        redis_cache = caches['default']
        redis_client = redis_cache.client.get_client()
        # print(redis_client.hgetall(1))
        # redis_client.hset(key=1, name=2022, value=str([client_ip, 'Hello']))
        # data = redis_client.hget(key=1, name=2022)
        # print(data)
        # data_list = data.decode('utf-8').strip('\"][\'\\').split(', ')
        # print(data_list)
        # data_list.append('Many')
        # redis_client.hset(key=1, name=2022, value=str(data_list))
        # data = redis_client.hget(key=1, name=2022)
        # data_list = data.decode('utf-8').strip('\"][\'\\').split(', ')
        # print(data)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        phone_numbers = request.data.getlist('phone_numbers')

        data = request.data

        context_data = {
            'images': images,
            'phone_numbers': phone_numbers,
        }

        serializer = self.get_serializer(data=data, context=context_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
