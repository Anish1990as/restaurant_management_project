from django.urls import path
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu_items, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('reservations/', views.reservation_page, name='reservations'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/thanks/', views.feedback_thanks, name='feedback_thanks'),
]