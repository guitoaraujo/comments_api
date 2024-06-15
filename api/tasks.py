from celery import shared_task
# from django.core.mail import send_mail

@shared_task
def test_task(subject, message, from_email, recipient_list):
    # send_mail(subject, message, from_email, recipient_list)
    print('ENVIANDO EMAIL...')
    print('EMAIL ENVIADO!')
