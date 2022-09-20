from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from config.celery import app

from decouple import config

from advertisement.models import Advertisement

User = get_user_model()


@app.task
def send_activation_mail(email, activation_code):
    message = {
        'email_subject': 'Activation Code',
        'email_body': f"Спасибо за регистрацию. Код активаций: {activation_code}",
        'to_whom': email
    }
    send_message_to_email.delay(message)


@app.task
def send_ads_for_emails():
    adverts = Advertisement.objects.all()[:10]
    email_body = []
    front_host = config('FRONT_HOST')

    for advert in adverts:
        email_body.append(f"{advert.name}-{front_host}{reverse('advertisement', kwargs={'pk': advert.pk})}")

    for user in User.objects.all():
        message = {
            'email_subject': 'Ежедневные объявления',
            'email_body': '\n'.join(email_body),
            'to_whom': user.email
        }
        send_message_to_email.delay(message)


@app.task
def send_message_to_email(message):
    send_mail(
        subject=message["email_subject"],
        message=message["email_body"],
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            message["to_whom"],
        ],
        fail_silently=True,
    )
