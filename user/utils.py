from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_activation_mail(email, activation_code, request):
    message = {
        'email_subject': 'Activation Code',
        'email_body': f"""Спасибо за регистрацию.
        Активируйте аккаунт: {activation_code}""",
        'to_whom': email
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
