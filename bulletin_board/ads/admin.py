from django.contrib import admin
from .models import Ads, Response, EmailKey

admin.site.register(Ads)
admin.site.register(Response)
admin.site.register(EmailKey)