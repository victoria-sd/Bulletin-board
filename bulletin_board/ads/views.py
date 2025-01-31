from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import SignUpForm, AdsForm, ResponseForm
from .models import Ads
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class AdsList(ListView):
    model = Ads
    ordering = 'title'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 2


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


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/registration/activation'
    template_name = 'registration/signup.html'


