import redis
import json

from django.conf import settings
from django.utils import timezone


def get_client_ip(request):
    """
    Get client ip by request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Redis:
    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def get_data(self, ads_id, date):
        """
        Get decoded data
        """
        byte_data = self.conn.get(ads_id)

        base_data = self.get_base_structure(date)

        if byte_data is None:
            data = base_data
        else:
            data = self.decode_data(byte_data)

        if not data.get(date):
            data[date] = self.get_base_data()

        return data

    def check_date(self, decoded_data, date) -> bool:
        """
        Check date in redis
        """
        if decoded_data.get(date):
            return True

        return False

    def check_ip(self, decoded_data, client_ip) -> bool:
        """
        Check client ip in redis
        """
        if client_ip in decoded_data['clients_ip']:
            return True
        return False

    def check_phone_ip(self, decoded_data, client_ip) -> bool:
        """
        Check client ip in phone view redis
        """
        if client_ip in decoded_data['phone_client_ip']:
            return True
        return False

    def check_data(self, decoded_data, date, client_ip) -> bool:
        """
        Check data by date and client ip
        Check client ip already exists or no
        """
        if not self.check_date(decoded_data, date):
            return False

        if not self.check_ip(decoded_data, client_ip):
            return False

        return True

    def check_phone_data(self, decoded_data, date, client_ip) -> bool:
        """
        Check phone_data by date and client ip
        """
        if not self.check_date(decoded_data, date):
            return False

        if not self.check_phone_ip(decoded_data, client_ip):
            return False

        return True

    def get_base_data(self):
        data = {
            'clients_ip': [],
            'phone_client_ip': [],
            'phone_views_count': 0,
            'views_count': 0
        }
        return data

    def get_base_structure(self, date):
        """
        Base structure for advertisement views
        """
        base_data = self.get_base_data()

        base_data_structure = {
            date: base_data,
            'clients_ip': [],
            'phone_client_ip': [],
            'phone_views_count': 0,
            'views_count': 0
        }
        return base_data_structure

    def add_views(self, ads_id, date, client_ip) -> None:
        """
        Add views for advertisement
        """
        data = self.get_data(ads_id, date)

        if not self.check_data(data, date, client_ip):
            data[date]['clients_ip'].append(client_ip)
            data[date]['views_count'] += 1

            data['clients_ip'].append(client_ip)
            data['views_count'] += 1
            self.conn.set(ads_id, json.dumps(data))

    def add_phone_views(self, ads_id, date, client_ip):
        """
        Add phone views for advertisement
        """
        data = self.get_data(ads_id, date)

        if not self.check_phone_data(data, date, client_ip):
            data[date]['phone_client_ip'].append(client_ip)
            data[date]['phone_views_count'] += 1

            data['phone_client_ip'].append(client_ip)
            data['phone_views_count'] += 1
            self.conn.set(ads_id, json.dumps(data))

    def get_ads_data(self, ads_id):
        """
        Get data by ads_id
        """
        byte_data = self.conn.get(ads_id)
        base_date = timezone.now().date().strftime('%d.%m.%Y')

        if not byte_data:
            data = self.get_base_structure(base_date)
            self.conn.set(ads_id, json.dumps(data))

        else:
            data = self.decode_data(byte_data)

        return data

    def decode_data(self, data):
        """
        Decode byte data
        """
        decode_data = data.decode('utf-8')
        data = json.loads(decode_data)
        return data

    def close(self):
        self.conn.close()
