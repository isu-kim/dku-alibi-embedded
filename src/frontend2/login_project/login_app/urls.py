# login_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('success/<username>/', views.success, name='success'),
]
