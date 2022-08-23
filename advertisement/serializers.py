from rest_framework import serializers

from .models import Category, ChildCategory, Advertisement, AdsSubscriber, AdsImage, City, Number, ViewStatistic


class AdvertisementSerializer(serializers.ModelSerializer):
    deleted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildCategory
        fields = '__all__'


class AdsSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSubscriber
        fields = '__all__'


class AdsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsImage
        fields = '__all__'


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = '__all__'


class ViewStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewStatistic
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
