from drf_yasg import openapi

category_id_query = openapi.Parameter('category_id', openapi.IN_QUERY, description='category id',
                                      type=openapi.TYPE_INTEGER)
has_image_query = openapi.Parameter('has_image', openapi.IN_QUERY, description='Has image', type=openapi.TYPE_BOOLEAN)
price_query = openapi.Parameter('price', openapi.IN_QUERY, description='Price', type=openapi.TYPE_INTEGER)
max_price_query = openapi.Parameter('max_price', openapi.IN_QUERY, description='Max price', type=openapi.TYPE_INTEGER)

limit_query = openapi.Parameter('limit', openapi.IN_QUERY, description='Simular advertisement count',
                                type=openapi.TYPE_INTEGER)

child_category_id_query = openapi.Parameter('child_category_id', openapi.IN_PATH, description='child category id',
                                            type=openapi.TYPE_INTEGER)
