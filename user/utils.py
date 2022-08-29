from django.core.mail import send_mail
from hashlib import md5
from config.settings import EMAIL_HOST_USER


def send_activation_mail(email, activation_code):
    message = f"""Спасибо за регистрацию. Активируйте аккаунт по ссылке:
    http://127.0.0.1:8000/api/activation/{activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'test@mysite.com',
        [email, ],
    )


def send_password_with_email(user: str) -> None:
    new_password = md5(user.email.encode()).hexdigest()
    user.set_password(new_password)
    user.save()
    data = {
        'email_subject': 'your new password',
        'email_body': f'Hi {user.first_name}\n your new password {new_password}',
        'to_whom': user.email,

    }
    Util.send_email(data)


class Util:
    @staticmethod
    def send_email(data):
        send_mail(
            subject=data["email_subject"],
            message=data["email_body"],
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                data["to_whom"],
            ],
            fail_silently=True,
        )
