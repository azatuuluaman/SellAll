import redis
import json

from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Redis:
    def __init__(self):
        self.conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def check_date(self, decoded_data, date) -> bool:
        return True if date == decoded_data['date'] else False

    def check_ip(self, decoded_data, client_ip) -> bool:
        return True if client_ip in decoded_data['clients_ips'] else False

    def add_view(self, ads_id, date, client_ip) -> None:
        byte_data = self.conn.get(ads_id)
        base_data = {
            date: {
                'clients_ip': client_ip,
                'count': 1
            },
            'clients_ip': [client_ip],
            'count': 1
        }

        if byte_data is None:
            self.conn.set(ads_id, json.dumps(base_data))
            return

        data = self.decode_data(byte_data)

        if not self.check_date(data, date):
            self.conn.set(ads_id, json.dumps(base_data))
            return

        data[date]['clients_ip'].append(client_ip)
        date[data]['count'] += 1

        data['clients_ip'].append(client_ip)
        data['count'] += 1

        self.conn.set(ads_id, json.dumps(data))

    def decode_data(self, data):
        decode_data = data.decode('utf-8')
        data = json.loads(decode_data)
        return data
