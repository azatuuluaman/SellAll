from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from config.settings import EMAIL_HOST_USER


def send_activation_mail(email, activation_code, request):
    current_site = get_current_site(request=request)
    message = {
        'email_subject': 'Activation Code',
        'email_body': f"""Спасибо за регистрацию.
        Активируйте аккаунт по ссылке:
        http://{current_site.domain}{reverse('activate', kwargs={'code': activation_code})}""",
        'to_whom': email
    }
    Util.send_email(message)


def send_password_with_email(user: str) -> None:
    new_password = get_random_string(8)
    user.set_password(new_password)
    user.save()
    message = {
        'email_subject': 'your new password',
        'email_body': f'Hi {user.first_name}\n your new password {new_password}',
        'to_whom': user.email,
    }
    Util.send_email(message)


class Util:
    @staticmethod
    def send_email(message):
        send_mail(
            subject=message["email_subject"],
            message=message["email_body"],
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                message["to_whom"],
            ],
            fail_silently=True,
        )
