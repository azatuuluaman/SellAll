from rest_framework import serializers

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


class AdvertisementListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    deleted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    child_category = serializers.CharField(source='child_category.name', read_only=True)
    owner = serializers.CharField(source='owner.email', read_only=True)
    images = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id',
                  'name',
                  'price',
                  'max_price',
                  'description',
                  'email',
                  'whatsapp_number',
                  'type',
                  'created_at',
                  'modified_at',
                  'deleted_at',
                  'city',
                  'child_category',
                  'owner',
                  'images'
                  )


class AdvertisementSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data.get('max_price'):
            if data['price'] >= data['max_price']:
                raise serializers.ValidationError({"max_price": "max_price can't be losses or equal than price!"})
        return data

    class Meta:
        model = Advertisement
        fields = '__all__'


class ChildCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = ChildCategory
        fields = ('id', 'name', 'category', 'ads_count')

    def get_ads_count(self, obj):
        return Advertisement.objects.filter(child_category=obj).count()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdsImageSerializer(serializers.ModelSerializer):
    advertisement = serializers.CharField(source='advertisement.name')

    class Meta:
        model = AdsImage
        fields = '__all__'


class AdsSubscriberSerializer(serializers.ModelSerializer):
    advertisement = serializers.CharField(source='advertisement.name')
    subscription = serializers.CharField(source='subscription.name')

    class Meta:
        model = AdsSubscriber
        fields = '__all__'


class NumberSerializer(serializers.ModelSerializer):
    advertisement = serializers.CharField(source='advertisement.name')

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
