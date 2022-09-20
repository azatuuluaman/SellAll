from rest_framework import serializers
from drf_yasg import openapi

limit_query = openapi.Parameter('limit', openapi.IN_QUERY, description='Simular advertisement count',
                                type=openapi.TYPE_INTEGER)

child_category_id_query = openapi.Parameter('child_category_id', openapi.IN_PATH, description='child category id',
                                            type=openapi.TYPE_INTEGER)


class AdvertisementQuerySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)
    has_image = serializers.BooleanField(required=False)
    price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)
    cities = serializers.ListField(required=False, child=serializers.IntegerField(min_value=1))
