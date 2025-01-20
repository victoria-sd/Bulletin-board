from django.urls import path
from .views import AdsList


urlpatterns = [
   path('', AdsList.as_view()),
]