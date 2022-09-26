from django.utils import timezone

from rest_framework import status, views
from rest_framework.response import Response

from advertisement.models import Advertisement
from advertisement.utils import Redis


class AddPhoneView(views.APIView):
    def get(self, request, *args, **kwargs):
        ads_id = self.kwargs.get('pk')
        ads = Advertisement.objects.filter(pk=ads_id).exists()

        if not ads:
            return Response({'message': 'Advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        redis = Redis()
        date = timezone.now().date().strftime('%d.%m.%Y')
        client_ip = request.ip
        redis.add_phone_views(ads_id, date, client_ip)
        redis.close()

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class StatisticsView(views.APIView):
    def get(self, request, *args, **kwargs):
        ads_id = self.kwargs['pk']
        ads = Advertisement.objects.filter(pk=ads_id).exists()

        if not ads:
            return Response({'message': 'Advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        redis = Redis()
        data = redis.get_ads_data(ads_id)
        redis.close()

        del data['clients_ip']
        del data['phone_client_ip']

        for key in data:
            if type(data[key]) == dict:
                del data[key]['clients_ip']
                del data[key]['phone_client_ip']

        return Response(data, status=status.HTTP_200_OK)
