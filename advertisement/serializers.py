from rest_framework import serializers

from .models import Category, ChildCategory, Advertisement, AdsSubscriber, AdsImage, City, Number, ViewStatistic


class AdvertisementSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    deleted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    child_category_name = serializers.CharField(source='child_category.name', read_only=True)
    owner_username = serializers.CharField(source='owner.email', read_only=True)
    images = serializers.StringRelatedField(many=True, read_only=True)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['price'] >= data['max_price']:
            raise serializers.ValidationError({"max_price": "max_price can't be losses or equal than price!"})
        return data

    class Meta:
        model = Advertisement
        fields = ('id',
                  'name',
                  'price',
                  'max_price',
                  'description',
                  'email',
                  'whatsapp_number',
                  'created_at',
                  'modified_at',
                  'deleted_at',
                  'city',
                  'city_name',
                  'child_category',
                  'child_category_name',
                  'owner',
                  'owner_username',
                  'images'
                  )


class AdsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsImage
        fields = '__all__'


class ChildCategorySerializer(serializers.ModelSerializer):
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = ChildCategory
        fields = ('id', 'name', 'category', 'ads_count')

    def get_ads_count(self, obj):
        return Advertisement.objects.filter(child_category=obj).count()


class CategorySerializer(serializers.ModelSerializer):
    # child_category = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon',)
        # 'child_category'


class AdsSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsSubscriber
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
