from rest_framework import serializers

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    AdsImage,
    City,
    PhoneNumber,
    ViewStatistic, AdsComment
)


class PhoneNumberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'phone_number')


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

    class Meta:
        model = AdsComment
        fields = ('user', 'advertisement', 'text', 'parent', 'children')


class AdvertisementListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    modified_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    deleted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    child_category = serializers.CharField(source='child_category.name', read_only=True)
    owner = serializers.CharField(source='owner.email', read_only=True)
    images = AdsImageListSerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberListSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    def get_comments(self, obj):
        instance = AdsComment.objects.filter(advertisement=obj, parent__isnull=True)
        return AdsCommentSerializer(instance, many=True).data

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
            'phone_numbers',
            'comments'
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
