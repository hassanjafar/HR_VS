from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
path('', include('django.contrib.auth.urls')),    
path('accounts/' , include('django.contrib.auth.urls'))
]