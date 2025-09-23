from django.shortcuts import render
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer


def order_confirmation(request):
    # Generate a sample order number (you can replace this with actual order id from DB)
    order_number = random.randint(10000, 99999)
    context = {
        'order_number': order_number
    }
    return render(request, 'orders/order_confirmation.html', context)

    
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)