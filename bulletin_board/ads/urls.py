from django.urls import path
from .views import AdsList, AdsDetail, AdsCreate, AdsUpdate

urlpatterns = [
   path('', AdsList.as_view(), name='ads_list'),
   path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
   path('create/', AdsCreate.as_view(), name='ads_create'),
   path('<int:pk>/update/', AdsUpdate.as_view(), name='ads_update'),
]
