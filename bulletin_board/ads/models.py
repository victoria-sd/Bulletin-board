from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
import secrets


class Ads(models.Model):  #объявления

    VARIANTS = [
        ('tank', "Танки"),
        ('healers', "Хилы"),
        ('dd', 'ДД'),
        ('trader', 'Торговцы'),
        ('guildmaster', 'Гилдмастеры'),
        ('questgiver', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion maker', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=12, choices=VARIANTS, default='tank')
    title = models.CharField(max_length=64)
    text = HTMLField()

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('ads_detail', args=[str(self.id)])


class Response(models.Model):  #отклики на объявления
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)


class EmailKey(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.code}'

    @staticmethod
    def generate_code():
        return secrets.token_urlsafe(32)