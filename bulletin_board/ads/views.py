from django.shortcuts import render
from django.views.generic import ListView
from .models import Ads


class AdsList(ListView):
    model = Ads
    ordering = 'title'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 5