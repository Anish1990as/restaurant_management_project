from django.urls import path
from .views import *
from .views import OrderHistoryView

app_name = "orders"

urlpatterns = [
    path("order-history/", OrderHistoryView.as_view(), name="order-history"),
    path("orders/", include("orders.urls", namespace="orders")),
]