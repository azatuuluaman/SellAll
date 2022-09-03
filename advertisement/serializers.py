from rest_framework import serializers

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    AdsImage,
    City,
    PhoneNumber,
    ViewStatistic
)


class PhoneNumberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'phone_number')


class AdsImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsImage
        fields = ('id', 'image')


class AdvertisementListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    deleted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    child_category = serializers.CharField(source='child_category.name', read_only=True)
    owner = serializers.CharField(source='owner.email', read_only=True)
    images = AdsImageListSerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberListSerializer(many=True, read_only=True)

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
            'whatsapp_number',
            'type',
            'created_at',
            'modified_at',
            'deleted_at',
            'city',
            'child_category',
            'owner',
            'images',
            'phone_numbers'
        )


class AdsImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsImage
        fields = ('image', 'advertisement')


class PhoneNumberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number', 'advertisement')


class AdvertisementSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        images = self.context.get('images')
        phone_numbers = self.context.get('phone_numbers')
        price = data.get('price')
        max_price = data.get('max_price')

        if max_price:
            if price >= max_price:
                raise serializers.ValidationError({"max_price": "max_price can't be losses or equal than price!"})

        if len(phone_numbers) < 1:
            raise serializers.ValidationError({"phone_numbers": "Phone number can't be less 1!"})

        if len(images) > 8:
            raise serializers.ValidationError({"images": "Images count can't be more 8!"})

        return data

    def create(self, validated_data):
        instance = super(AdvertisementSerializer, self).create(validated_data)
        instance.save()

        images = self.context.get('images')
        phone_numbers = self.context.get('phone_numbers')

        for image in images:
            AdsImage.objects.create(advertisement=instance, image=image)

        for phone_number in phone_numbers:
            PhoneNumber.objects.create(advertisement=instance, phone_number=phone_number)

        return instance

    class Meta:
        model = Advertisement
        fields = (
            'name',
            'price',
            'max_price',
            'description',
            'email',
            'whatsapp_number',
            'type',
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
        return Advertisement.objects.filter(child_category=obj).count()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdsSubscriberSerializer(serializers.ModelSerializer):
    advertisement = serializers.CharField(source='advertisement.name')
    subscription = serializers.CharField(source='subscription.name')

    class Meta:
        model = AdsSubscriber
        fields = '__all__'


class ViewStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewStatistic
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
