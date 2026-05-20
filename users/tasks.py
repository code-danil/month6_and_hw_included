from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.utils import timezone
from django.contrib.auth import get_user_model


@shared_task
def add(x, y):
    print(f'args: {x} and {y}---------------------------------->')
    # return x + y 
    # from time import sleep
        
    # sleep(15)
    return x + y


@shared_task
def send_otp_mail(email, otp):
    print('settings ' * 10)
    send_mail(
        subject='YOUR OTP code',
        message=f'otp code{otp}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,

    )
    return 'OK'





@shared_task
def send_report_mail():
    print('settings ' * 10)
    send_mail(
        subject='Report data',
        message=f'что то спуер пупер важное',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            'riszav.01@gmail.com', 
            'azi.99kg.tls@gmail.com',
            'bkaizirek2002@gmail.com',
            'abdillaevamedina6@gmail.com',

        ],
        fail_silently=False,

    )
    return 'OK'


# Это Домашний задание!
@shared_task
def generate_promo_code(user_email):
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    print(f'Промокод: {code} создан для {user_email}')
    return code



@shared_task
def send_daily_stats():
    User = get_user_model()
    count = User.objects.count()
    send_mail(
        subject='Ежденевная статистика',
        message=f'Всего пользователей на сайте: {count}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['admin@gmail.com'],
        fail_silently=False,
    )
    return 'OK'


@shared_task
def send_welcome_email(user_email):
    send_mail(
        subject='Добро пожаловать!',
        message='Спасибо за регистрацию на нашем сайте!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return 'OK'