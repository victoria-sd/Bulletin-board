from django.urls import path
from .views import SignUp, login_view, login_with_code, profile_view, response_view, delete_response, approve_response

urlpatterns = [
    path('login/', login_view, name='login'),
    path('activation/', login_with_code, name='activation'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/response/', response_view, name='response'),
    path('profile/response/<int:response_id>/delete/', delete_response, name='delete_response'),
    path('profile/response/<int:response_id>/approve/', approve_response, name='approve_response'),
    # path('profile/', ProfileDetail.as_view(), name='profile'),

]
