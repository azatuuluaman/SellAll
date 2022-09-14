from django.utils import timezone

from rest_framework import status, views
from rest_framework.response import Response

from advertisement.models import Advertisement
from advertisement.utils import Redis, get_client_ip


class AddPhoneView(views.APIView):
    def get(self, request, *args, **kwargs):
        ads_id = self.kwargs.get('pk')
        ads = Advertisement.objects.filter(pk=ads_id).exists()

        if not ads:
            return Response({'message': 'Advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        redis = Redis()
        date = timezone.now().date().strftime('%d.%m.%Y')
        client_ip = get_client_ip(request)
        redis.add_phone_views(ads_id, date, client_ip)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class StatisticsView(views.APIView):
    def get(self, request, *args, **kwargs):
        ads_id = self.kwargs['pk']
        ads = Advertisement.objects.filter(pk=ads_id).exists()

        if not ads:
            return Response({'message': 'Advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        redis = Redis()
        data = redis.get_ads_data(ads_id)
        return Response(data, status=status.HTTP_200_OK)
