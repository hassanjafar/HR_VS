from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView


#to use {% url 'store_app:dashboard' %}

app_name='ID_App'
urlpatterns = [
    
     path('users/', LoginView.as_view(template_name='users/index.html'), name='index'),
     path('gatetwores/', views.gatetwo, name='gatetwo'),
     path('gatetwo/', views.callapi, name='callapi'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('dashrepot/',views.dash_report, name='dash_report'),
     path('gate_two/', views.gatetwohorizantal, name='gatetwohorizantal'),
     path('report/', views.report, name="report"),
     path('reports/', views.reports, name="reports"),
     path('reportgenerate/', views.pdf_generate, name="pdf_generate"),
     path('idapp/', views.dashboard, name="dashboard"),
     path('logout/', views.logout, name="logout"),
     path('profilereport/',views.pdf_response,name="pdf_response"),
     path('', views.login, name="login")



    
 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)