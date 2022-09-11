from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, status, views
from rest_framework.filters import OrderingFilter, SearchFilter, BaseFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

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
    permission_classes = (AllowAny,)

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter, AdvertisementPriceFilterBackend)
    filterset_fields = ('child_category', 'city', 'disable_date')
    search_fields = ('name',)
    ordering_fields = ('created_at', 'price')

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = AdvertisementSerializer

        if self.action in ['list', 'retrieve']:
            serializer_class = AdvertisementRetrieveSerializer

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
        redis = Redis()
        ads_id = instance.pk
        date = timezone.now().date().strftime('%d.%m.%Y')
        client_ip = get_client_ip(request)

        redis.add_views(ads_id, date, client_ip)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        data = request.data

        context_data = {
            'images': images,
        }

        serializer = self.get_serializer(data=data, context=context_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.disable_date = True
        instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


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
