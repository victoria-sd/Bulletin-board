from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import AdsForm, ResponseForm
from .models import Ads
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class AdsList(ListView):
    model = Ads
    ordering = '-created_at'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 3


class AdsDetail(DetailView):
    model = Ads
    template_name = 'ad.html'
    context_object_name = 'ad'

    def post(self, request, *args, **kwargs):
        ads = self.get_object()
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ads
            response.author = self.request.user
            response.save()
            messages.success(request, 'Ваш отклик отправлен. Он отобразится на главной странице после того, как автор примет его.')
        return redirect('ads_detail', pk=ads.pk)


class AdsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('ads.add_ads',)
    form_class = AdsForm
    model = Ads
    template_name = 'ads_create.html'


class AdsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('ads.change_ads',)
    form_class = AdsForm
    model = Ads
    template_name = 'ads_create.html'



