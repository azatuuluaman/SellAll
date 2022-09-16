from rest_framework import generics

from advertisement.serializers import (
    CitySerializer,
    CategorySerializer,
    ChildCategorySerializer,
    AdsSubscriberSerializer,
    CategoryDetailSerializer
)

from advertisement.models import (
    Category,
    ChildCategory,
    AdsSubscriber,
    City,
)


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

