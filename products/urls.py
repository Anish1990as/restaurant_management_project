from django.urls import path, include
from .views import *

urlpatterns = [
    path("", include("home.urls")),
    path('items/', ItemView.as_view(), name='item-list-create'),
    path('menu/', views.menu_list, name='menu'), 
    path('menu/', views.menu_view, name='menu'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)