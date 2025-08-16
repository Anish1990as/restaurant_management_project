from django.urls import path
from .views import *

urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list'),
    path('product/<int:product_id>/', get_product, name='get-product'),
]