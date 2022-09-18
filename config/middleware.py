from django.utils import timezone

from rest_framework.generics import get_object_or_404

from advertisement.models import Advertisement
from advertisement.views.advertisement_views import AdvertisementRUDView
from advertisement.utils import get_client_ip, Redis


class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = get_client_ip(request)
        request.user.ip = user_ip
        response = self.get_response(request)

        return response


class ViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.cls == AdvertisementRUDView and request.method == 'GET':
            pk = view_kwargs.get('pk', None)
            instance = get_object_or_404(Advertisement, pk=pk)
            redis = Redis()
            ads_id = instance.pk
            date = timezone.now().date().strftime('%d.%m.%Y')
            client_ip = request.user.ip
            redis.add_views(ads_id, date, client_ip)
