from django.conf import settings
from rest_framework import serializers
from drf_yasg import openapi

# category_id_query = openapi.Parameter('category_id', openapi.IN_QUERY, description='category id',
#                                       type=openapi.TYPE_INTEGER)
# has_image_query = openapi.Parameter('has_image', openapi.IN_QUERY, description='Has image', type=openapi.TYPE_BOOLEAN)
# price_query = openapi.Parameter('price', openapi.IN_QUERY, description='Price', type=openapi.TYPE_INTEGER)
# max_price_query = openapi.Parameter('max_price', openapi.IN_QUERY, description='Max price', type=openapi.TYPE_INTEGER)
# cities_query = openapi.Parameter('cities', openapi.IN_QUERY, description='Cities array', type=openapi.TYPE_ARRAY,
#                                  items=openapi.Items(type=openapi.TYPE_STRING))
#
limit_query = openapi.Parameter('limit', openapi.IN_QUERY, description='Simular advertisement count',
                                type=openapi.TYPE_INTEGER)

child_category_id_query = openapi.Parameter('child_category_id', openapi.IN_PATH, description='child category id',
                                            type=openapi.TYPE_INTEGER)


# subscription_query = openapi.Parameter('subscription', openapi.IN_QUERY, description='', openapi.TYPE_STRING)

class AdvertisementQuerySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)
    has_image = serializers.BooleanField(required=False)
    price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)
    cities = serializers.ListField(required=False, child=serializers.IntegerField(min_value=1))
