from django.urls import path, include
from .views import *
from . import views

urlpatterns = [
    path("", include("home.urls")),
    path('items/', ItemView.as_view(), name='item-list-create'),
    path('menu/', views.menu_list, name='menu'), 
    path('menu/', views.menu_view, name='menu'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)