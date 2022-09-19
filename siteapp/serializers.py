from rest_framework import serializers

from .models import Site, SocialMedia, FeedBack, Help, HelpCategory


class SiteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Site
        fields = '__all__'


class SocialMediaSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = SocialMedia
        fields = '__all__'

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ('name', 'email', 'subject', 'text')


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'


class HelpCategorySerializer(serializers.ModelSerializer):
    help = serializers.SerializerMethodField(read_only=True)

    def get_help(self, obj):
        instance = Help.objects.filter(category=obj)
        return HelpSerializer(instance, many=True).data

    class Meta:
        model = HelpCategory
        fields = ('id', 'name', 'help')

# class FooterCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name')
#
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data


# class FooterCitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = City
#         fields = ('id', 'name')
#
#     def to_representation(self, value):
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         return serializer.data


# class FooterSerializer(serializers.Serializer):
#     category = FooterCategorySerializer(many=True, read_only=True)
#     city = FooterCitySerializer(many=True, read_only=True)
#     app = SocialMediaSerializer(many=True, read_only=True)
#     network = SocialMediaSerializer(many=True, read_only=True)
#
#     class Meta:
#         fields = (
#             'category',
#             'city',
#             'app',
#             'network',
#         )
