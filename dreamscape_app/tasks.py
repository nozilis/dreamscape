from django.core.mail import send_mail
from celery import shared_task
from decouple import config

@shared_task
def greetings_email(email):
    send_mail(
        subject = 'Доброй пожаловать, Мечтатель!',
        message = 'Приветствует и благодарим за вашу регистрацию в приложении Dreamscape, желаем приятного использования и скорейшего исполнения ваших желаний!',
        from_email = config('FROM_EMAIL'),  
        recipient_list = [email], 
        fail_silently = False  
    )