from hashlib import md5
from urllib.parse import urlencode
from django.conf import settings


class PayboxRedirectService:
    """
    Operating for request to paybox,
    used when a client pays for his site at a tariff,
    """

    @classmethod
    def generate_paybox_url(cls, donate):
        """generate url for redirect to paybox for payment site rent"""

        paybox_params = {
            "pg_merchant_id": settings.PAYBOX_PROJECT_ID,
            "pg_amount": str(donate.amount),
            "pg_currency": settings.PAYBOX_CURRENCY,
            "pg_payment_id": str(donate.id),
            "pg_order_id": str(donate.id),
            "pg_salt": settings.PAYBOX_SALT,
            "pg_description": str(donate.user_name),
            "pg_language": settings.PAYBOX_LANGUAGE,
            # "pg_success_url": settings.PG_SITE_URL + "donate/" + str(donate.id),
            # "pg_success_url_method": settings.PAYBOX_SUCCESS_URL_METHOD,
            # "pg_result_url": settings.PAYBOX_RESULT_URL,
            "secret_key": settings.PAYBOX_SECRET_KEY,
            # "pg_failure_url": settings.PG_SITE_URL + "donate/" + str(donate.id),
            "pg_testing_mode": "1",
        }
        paybox_params = dict(sorted(paybox_params.items()))
        pg_sig_gen = cls.generate_sig(paybox_params.values())
        paybox_params["pg_sig"] = pg_sig_gen

        # secret_key used just for generation pg_sig(*подпись)
        del paybox_params["secret_key"]
        url_params = urlencode(paybox_params)

        return f"{settings.PAYBOX_URL}?{url_params}"

    @staticmethod
    def generate_sig(sig_params):
        result = ["payment.php", ";".join(sig_params)]
        pg_sig = ";".join(result)
        pg_sig = md5(pg_sig.encode("UTF-8")).hexdigest()

        return pg_sig
