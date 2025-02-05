import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from ads.models import EmailKey, Ads, Response
from django.contrib.auth.decorators import login_required


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login/'
    template_name = 'registration/signup.html'


@login_required
def profile_view(request): #представление личного кабинета
    user = request.user
    ads = Ads.objects.filter(author=user).order_by('-created_at')
    return render(request, 'account/profile.html', {'user': user, 'ads': ads})


@login_required
def response_view(request): #представление с откликами
    user = request.user
    ads = Ads.objects.filter(author=user).order_by('-created_at')

    selected_ad_id = request.GET.get('ad', None)
    responses = []
    if selected_ad_id:
        responses = Response.objects.filter(ad_id=selected_ad_id).order_by('-created_at')
    else:
        for ad in ads:
            responses += list(ad.response.all())

    return render(request, 'account/response.html', {'user': user, 'ads': ads, 'responses': responses, 'selected_ad_id': selected_ad_id})


@login_required
def delete_response(request, response_id): #удаление отклика

    response = get_object_or_404(Response, id=response_id)

    if request.user == response.ad.author:
        if request.method == "POST":
            response.delete()
            return redirect('response')
        return render(request, 'account/delete_response.html', {'response': response})
    else:
        return HttpResponseForbidden("У вас нет прав для удаления этого комментария.")


@login_required
def approve_response(request, response_id): #принятие отклика

    response = get_object_or_404(Response, id=response_id)

    if request.user == response.ad.author:
        if request.method == "POST":
            response.approved = True
            response.status = True
            response.save()
            return redirect('response')  # Перенаправление на страницу со списком комментариев
        return render(request, 'account/approve_response.html', {'response': response})
    else:
        return HttpResponseForbidden("У вас нет прав для принятия этого комментария.")


def login_view(request): #генерирование и отправка одноразового пароля при авторизации
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            one_time_code = EmailKey.generate_code()
            emailkey = EmailKey.objects.create(code=one_time_code, user=user)

            send_mail(
                subject='Одноразовый код.',
                message=f'Для подтверждения почты введите одноразовый код: {one_time_code}',
                from_email=None,
                recipient_list=[user.email],
            )
            return redirect('activation')

    return render(request, 'registration/login.html')


def login_with_code(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')

        try:
            email_key = EmailKey.objects.get(code=otp_code)
            user = email_key.user

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            email_key.delete()
            return redirect('profile')

        except EmailKey.DoesNotExist:
            return render(request, 'registration/activation.html', {'error': 'Invalid or used code'})

    return render(request, 'registration/activation.html')
