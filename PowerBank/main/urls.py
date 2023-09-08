from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'main'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_pw/', views.change_pw, name='change_pw'),
    path('remit/', views.remit, name='remit'),
    path('balance/', views.balance, name='balance'),
    path('log/', views.log, name='log'),
    path('gmoney/', views.gmoney, name='gmoney'),
]