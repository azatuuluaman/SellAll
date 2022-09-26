from django.conf import settings
from django.utils import timezone

from rest_framework import serializers

from user.serializers import UserSerializer
from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    AdsImage,
    City,
    AdsComment,
    ComplainingForAds,
    Favorite
)
from .utils import Redis


class AdsImageListSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = AdsImage
        fields = ('id', 'image')


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class AdsCommentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True, read_only=True)
    parent_id = serializers.IntegerField(required=False)

    def validate_parent(self, parent):
        if parent == 0:
            return None

        return parent

    class Meta:
        model = AdsComment
        fields = ('id', 'user', 'advertisement', 'text', 'parent_id', 'children')


class AdsSubscriberSerializer(serializers.ModelSerializer):
    subscription = serializers.CharField(source='subscription.name')

    class Meta:
        model = AdsSubscriber
        fields = ('subscription', 'start_date', 'end_date')


class AdvertisementRetrieveSerializer(serializers.ModelSerializer):
    views_count = serializers.SerializerMethodField()
    phone_view_count = serializers.SerializerMethodField()
    city = serializers.CharField(source='city.name', read_only=True)
    child_category = serializers.CharField(source='child_category.name', read_only=True)
    images = AdsImageListSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    subscribers = serializers.SerializerMethodField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(source='child_category.category.name', read_only=True)
    owner = UserSerializer(read_only=True)

    def get_is_favorite(self, obj):
        user = self.context.get('request').user

        if not user.is_authenticated:
            return False

        instance = Favorite.objects.prefetch_related('advertisement').filter(user=user, advertisement=obj)

        if not instance:
            return False

        return True

    def get_subscribers(self, obj):
        date = timezone.now()
        instance = AdsSubscriber.objects.filter(advertisement=obj, end_date__gte=date)
        return AdsSubscriberSerializer(instance, many=True).data

    def get_comments(self, obj):
        instance = AdsComment.objects.filter(advertisement=obj, parent__isnull=True)
        return AdsCommentSerializer(instance, many=True).data

    def get_views_count(self, obj):
        redis = Redis()
        data = redis.get_ads_data(obj.pk)
        redis.close()

        return data['views_count']

    def get_phone_view_count(self, obj):
        redis = Redis()
        data = redis.get_ads_data(obj.pk)
        redis.close()

        return data['phone_views_count']

    class Meta:
        model = Advertisement
        fields = (
            'id',
            'name',
            'slug',
            'price',
            'max_price',
            'description',
            'email',
            'phone_numbers',
            'whatsapp_number',
            'type',
            'views_count',
            'phone_view_count',
            'created_at',
            'modified_at',
            'disable_date',
            'city',
            'category',
            'child_category',
            'subscribers',
            'is_favorite',
            'owner',
            'images',
            'comments'
        )


class AdsImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsImage
        fields = ('image', 'advertisement')


class AdvertisementSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.ListField(required=False, allow_null=True)

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        images = self.context.get('images')
        owner = self.context.get('owner')

        price = data.get('price')
        max_price = data.get('max_price')

        if max_price:
            if price >= max_price:
                raise serializers.ValidationError({"max_price": "max_price can't be losses or equal than price!"})

        if len(images) > 8:
            raise serializers.ValidationError({"images": "Images count can't be more 8!"})

        data['owner'] = owner

        return data

    def create(self, validated_data):
        instance = super(AdvertisementSerializer, self).create(validated_data)
        instance.save()
        images = self.context.get('images')

        for image in images:
            AdsImage.objects.create(advertisement=instance, image=image)

        return instance

    class Meta:
        model = Advertisement
        fields = (
            'name',
            'price',
            'max_price',
            'description',
            'email',
            'phone_numbers',
            'whatsapp_number',
            'city',
            'child_category',
            'owner',
        )


class ChildCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = ChildCategory
        fields = ('id', 'name', 'category', 'ads_count')

    def get_ads_count(self, obj):
        return Advertisement.objects.filter(child_category=obj, type=settings.ACTIVE).count()


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    child_category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'child_category')

    def get_child_category(self, obj):
        queryset = ChildCategory.objects.filter(category=obj)
        return ChildCategorySerializer(queryset, many=True).data

    def get_icon(self, obj):
        return obj.icon.url


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class ComplainingForAdsSerializer(serializers.ModelSerializer):
    advertisement_name = serializers.CharField(source='advertisement.name', read_only=True, default='')

    def validate(self, attrs):
        type = attrs.get('type')
        text = attrs.get('text')

        if type == settings.OTHER and not text:
            raise serializers.ValidationError('Другое должен иметь текст!')

        return attrs

    class Meta:
        model = ComplainingForAds
        fields = ('id', 'advertisement', 'advertisement_name', 'type', 'text', 'send_date')
