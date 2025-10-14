from django.shortcuts import render
import random
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from utils.email_utils import send_order_confirmation_email
from django.utils import timezone
from .models import Coupon
from .serializers import CouponSerializer
from rest_framework import status
from .serializers import OrderStatusUpdateSerializer
 

class CancelOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order_id = kwargs.get("pk")   
            order = Order.objects.get(pk=order_id, customer=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or not yours."},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status in ["completed", "cancelled"]:
            return Response(
                {"error": f"Order already {order.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = "cancelled"
        order.save()

        serializer = self.get_serializer(order)
        return Response(
            {"message": "Order cancelled successfully", "order": serializer.data},
            status=status.HTTP_200_OK
        )


 
def order_confirmation(request):
    
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


 
def create_order(request):
    
    order = Order.objects.create(...)  

   
    email_response = send_order_confirmation_email(
        order_id=order.id,
        customer_email=order.user.email,
        customer_name=order.user.username,
        total_amount=order.total_price
    )

    return Response({
        "order_id": order.id,
        "email_status": email_response
    })

 
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


class CouponValidationView(APIView):
    """
    POST endpoint to validate a coupon code.
    Request body: {"code": "SAVE10"}
    """
    def post(self, request):
        code = request.data.get('code')

        if not code:
            return Response({"error": "Coupon code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return Response({"error": "Invalid coupon code."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()

        # Validate coupon status and date
        if not coupon.is_active:
            return Response({"error": "This coupon is not active."}, status=status.HTTP_400_BAD_REQUEST)

        if not (coupon.valid_from <= today <= coupon.valid_until):
            return Response({"error": "This coupon is expired or not yet valid."}, status=status.HTTP_400_BAD_REQUEST)

        # If valid, return discount percentage
        return Response({
            "message": "Coupon is valid.",
            "code": coupon.code,
            "discount_percentage": float(coupon.discount_percentage)
        }, status=status.HTTP_200_OK)


class UpdateOrderStatusAPIView(APIView):
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Order status updated successfully.",
                "order_id": order.id,
                "new_status": serializer.data['status']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)