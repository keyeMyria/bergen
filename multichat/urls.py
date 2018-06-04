from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import index

urlpatterns = [
    path('', index),
    path('accounts/login/', login),
    path('accounts/logout/', logout),
    path('admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
