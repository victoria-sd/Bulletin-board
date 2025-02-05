from django import forms
from .models import Ads, Response


class AdsForm(forms.ModelForm):
    # author = forms.CharField(initial=User.username)

    class Meta:
        model = Ads
        fields = ['title', 'text', 'category', 'author']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория',
            'author': 'Автор'
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]