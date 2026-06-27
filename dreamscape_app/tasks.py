from django.core.mail import send_mail
from celery import shared_task
from decouple import config
from .models import Wish

@shared_task
def greetings_email(email):
    send_mail(
        subject = 'Доброй пожаловать, Мечтатель!',
        message = 'Приветствует и благодарим за вашу регистрацию в приложении Dreamscape, желаем приятного использования и скорейшего исполнения ваших желаний!',
        from_email = config('FROM_EMAIL'),  
        recipient_list = [email], 
        fail_silently = False  
    )

@shared_task
def dreaming_status_reminder():
    dreaming_status = Wish.objects.select_related('user').filter(status__exact='dreaming')
    for wish in dreaming_status:
        email = wish.user.email
        send_mail(
            subject = 'Ваша мечта в ожидании, Мечтатель!',
            message = 'Напоминаем Вам, что ваша мечта находится в ожидании исполнения!',
            from_email = config('FROM_EMAIL'),  
            recipient_list = [email], 
            fail_silently = False  
        )