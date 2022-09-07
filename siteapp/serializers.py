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
