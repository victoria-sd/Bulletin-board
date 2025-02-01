import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from ads.models import EmailKey


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = 'login.html'
    template_name = 'registration/signup.html'


class ProfileDetail(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'profile'


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # one_time_code = EmailKey.objects.create(code=random.choice('123456789'), user=user)
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

            login(request, user)
            email_key.delete()  # Delete the used one-time key
            return redirect('profile')  # Redirect to a profile or success page

        except EmailKey.DoesNotExist:
            return render(request, 'activation.html', {'error': 'Invalid or used code'})

    return render(request, 'activation.html')


