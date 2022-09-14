from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_activation_mail(email, activation_code):
    message = {
        'email_subject': 'Activation Code',
        'email_body': f"Спасибо за регистрацию. Код активаций: {activation_code}",
        'to_whom': email
    }
    send_message_to_email(message)


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
