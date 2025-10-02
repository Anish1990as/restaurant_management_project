from django.urls import path
from .views import *
from .views import OrderHistoryView
from .views import OrderDetailView
from .views import CancelOrderView

app_name = "orders"

urlpatterns = [
    path("order-history/", OrderHistoryView.as_view(), name="order-history"),
    path("orders/", include("orders.urls", namespace="orders")),
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path("cancel/<int:pk>/", CancelOrderView.as_view(), name="cancel-order"),
]