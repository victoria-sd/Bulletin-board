from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Ads, Response


@receiver(post_save, sender=Ads)
def ad_created(instance, created, **kwargs): #новостная рассылка при добавлении нового объявления
    if not created:
        return

    subject = f'Новое объявление'

    text_content = (
        f'Заголовок: {instance.title}\n'
        f'Содержание: {instance.text}\n\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'Заголовок: {instance.title}<br>'
        f'Содержание: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )

    msg = EmailMultiAlternatives(subject, text_content, None, [User.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Response)
def notification_about_response(sender, instance, created, **kwargs):
    if created:
        email = instance.ad.author.email
        send_mail(
            subject='Новый отзыв!',
            message=f'На ваше объявление {instance.ad} оставили новый отзыв!: {instance.text}',
            from_email=None,
            recipient_list=[email],
        )
