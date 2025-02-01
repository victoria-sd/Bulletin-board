from django.urls import path
from .views import SignUp, ProfileDetail, login_view, login_with_code

urlpatterns = [
    path('login/', login_view, name='registration/login'),
    path('activation/', login_with_code, name='registration/activation'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', ProfileDetail.as_view(), name='profile'),
]
