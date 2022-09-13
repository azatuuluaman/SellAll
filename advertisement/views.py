from django.conf import settings
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework import generics, status, views
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from .swagger_scheme import category_id, has_image, price, max_price
from .permissions import IsOwnerOrSuperUser, IsAuthorComment

from .serializers import (
    AdvertisementSerializer,
    AdvertisementRetrieveSerializer,
    CitySerializer,
    CategorySerializer,
    ChildCategorySerializer,
    AdsSubscriberSerializer,
    AdsCommentSerializer,
    CategoryDetailSerializer
)

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    City,
    AdsComment
)
from .utils import Redis, get_client_ip


class AdvertisementCustomFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        category_id = request.query_params.get('category_id')
        price = request.query_params.get('price')
        max_price = request.query_params.get('max_price')
        has_image = request.query_params.get('has_image')
        filters = {}

        if category_id:
            filters['child_category__category_id'] = category_id

        if has_image == 'True':
            filters['images__isnull'] = False

        if price and max_price:
            price = Q(price__gte=price)
            max_price = Q(max_price__lte=max_price)
            queryset = queryset.filter(price & max_price).filter(**filters).distinct()
            return queryset

        else:
            if price:
                filters['price__gte'] = price
            if max_price:
                filters['max_price__lte'] = max_price

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
        }

        serializer = self.get_serializer(data=data, context=context_data)
        serializer.is_valid(raise_exception=True)

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

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementListView(generics.ListAPIView):
    serializer_class = AdvertisementRetrieveSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementCustomFilterBackend)
    filterset_fields = ('child_category_id', 'city', 'disable_date')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    @swagger_auto_schema(method='get', manual_parameters=[category_id, has_image, price, max_price])
    @action(['get'], detail=False)
    def get(self, request, *args, **kwargs):
        return super(AdvertisementListView, self).get(request)

    def get_queryset(self):
        queryset = Advertisement.objects.filter(type=settings.ACTIVE)
        return queryset


class CityAPIView(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()


class ChildCategoryAPIView(generics.ListAPIView):
    serializer_class = ChildCategorySerializer
    queryset = ChildCategory.objects.all()


class AdsSubscriberAPIView(generics.ListAPIView):
    serializer_class = AdsSubscriberSerializer
    queryset = AdsSubscriber.objects.all()


class AdsCommentCreateView(generics.CreateAPIView):
    serializer_class = AdsCommentSerializer
    permission_classes = [IsAuthenticated]


class AdsCommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdsCommentSerializer
    queryset = AdsComment.objects.all()
    permission_classes = [IsAuthorComment]


class AddPhoneView(views.APIView):
    def get(self, request, *args, **kwargs):
        ads_id = self.kwargs.get('pk')
        ads = Advertisement.objects.filter(pk=ads_id).exists()

        if not ads:
            return Response({'message': 'Advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        redis = Redis()
        date = timezone.now().date().strftime('%d.%m.%Y')
        client_ip = get_client_ip(request)
        redis.add_phone_views(ads_id, date, client_ip)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class StatisticsView(views.APIView):
    def get(self, request, *args, **kwargs):
        ads_id = self.kwargs['pk']
        ads = Advertisement.objects.filter(pk=ads_id).exists()

        if not ads:
            return Response({'message': 'Advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        redis = Redis()
        data = redis.get_ads_data(ads_id)
        return Response(data, status=status.HTTP_200_OK)
