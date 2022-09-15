from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_message_to_email(message):
    send_mail(
        subject=message["email_subject"],
        message=message["email_body"],
        from_email=EMAIL_HOST_USER,
        recipient_list=[
            message["to_whom"],
        ],
        fail_silently=True,
    )
