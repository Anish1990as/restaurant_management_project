from django.urls import path
from .views import *

urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list-create'),
    path("menu/", views.menu_list, name="menu"), 
]