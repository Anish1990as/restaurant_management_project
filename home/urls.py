from django.urls import path
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('homepage/', homepage, name='homepage'),
]