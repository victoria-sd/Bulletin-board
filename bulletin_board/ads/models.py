from django.contrib.auth.models import User
from django.db import models


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
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=12, choices=VARIANTS, default='tank')
    title = models.CharField(max_length=64)
    text = models.TextField()
    # upload = models.FileField(upload_to='uploads/')

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return self.title


class Response(models.Model):  #отклики на объявления
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)
