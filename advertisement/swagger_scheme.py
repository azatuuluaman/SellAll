from drf_yasg import openapi

child_category_id = openapi.Parameter('child_category_id', openapi.IN_QUERY, description="child_category_id",
                                      type=openapi.TYPE_INTEGER)
has_image = openapi.Parameter('has_image', openapi.IN_QUERY, description='Has image', type=openapi.TYPE_BOOLEAN)
price = openapi.Parameter('price', openapi.IN_QUERY, description='Price', type=openapi.TYPE_INTEGER)
max_price = openapi.Parameter('max_price', openapi.IN_QUERY, description='Max price', type=openapi.TYPE_INTEGER)