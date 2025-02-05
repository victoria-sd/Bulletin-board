from django.contrib.auth import login
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from ads.models import EmailKey, Ads, Response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group


def signup_view(request): #регистрация пользователя, генерирование и отправка одноразового кода на почту
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            one_time_code = EmailKey.generate_code()
            emailkey = EmailKey.objects.create(code=one_time_code, user=user)

            send_mail(
                subject='Одноразовый код.',
                message=f'Для подтверждения почты введите одноразовый код: {one_time_code} по ссылке http://127.0.0.1:8000/accounts/activation/',
                from_email=None,
                recipient_list=[user.email],
            )
            return redirect('activation')
    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


def login_with_code(request): #авторизация пользователя через одноразовый код
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')

        try:
            email_key = EmailKey.objects.get(code=otp_code)
            user = email_key.user
            user.is_active = True
            user.save()
            authorized_user = Group.objects.get(name="authorized user") #после авторизации пользователь попадает в грппу "authorized user" с правами добавлять и изменять объявления
            user.groups.add(authorized_user)

            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            email_key.delete()
            return redirect('profile')

        except EmailKey.DoesNotExist:
            messages.error(request, 'Недействительный код подтверждения.')
            return redirect('activation')

    return render(request, 'registration/activation.html')


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
            return redirect('response')
        return render(request, 'account/approve_response.html', {'response': response})
    else:
        return HttpResponseForbidden("У вас нет прав для принятия этого комментария.")
