from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class AdvertisementCustomFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        category_id = request.query_params.get('category_id')
        price = request.query_params.get('price')
        max_price = request.query_params.get('max_price')
        has_image = request.query_params.get('has_image')
        cities = request.query_params.get('cities')

        filters = {}

        if category_id:
            filters['child_category__category_id'] = category_id

        if has_image == 'true':
            filters['images__isnull'] = False

        if cities:
            filters['city__in'] = cities.split(',')

        if price and max_price:
            min_price_filter = Q(price__gte=price)
            max_price_filter = Q(price__lte=max_price)
            queryset_1 = queryset.filter(min_price_filter & max_price_filter, **filters)
            queryset_2 = queryset_1.filter(max_price__lte=max_price, max_price__isnull=False)
            queryset = queryset_1 | queryset_2
            return queryset.distinct()
        else:
            if price:
                filters['price__gte'] = price

            if max_price:
                min_price = Q(price__lte=max_price)
                max_price = Q(max_price__lte=max_price)

                queryset = queryset.filter(min_price | max_price).filter(**filters).distinct()
                return queryset

        queryset = queryset.filter(**filters).distinct()

        return queryset
