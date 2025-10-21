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


ChatGPT said:
Perfect 👍 — let’s create your DRF API View for updating an order’s status (using a POST request this time).
We’ll implement it cleanly in 5 steps, exactly as you described.

✅ Step 1: Update Order Model
In your orders/models.py, make sure your model includes a status field with valid choices:

# orders/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
✅ Step 2: Create the API View
Now open orders/views.py and add this:

# orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order

class OrderStatusUpdateAPIView(APIView):
    """
    API endpoint to update the status of an existing order.
    Accepts POST request with 'order_id' and 'status'.
    """

    def post(self, request):
        order_id = request.data.get('order_id')
        new_status = request.data.get('status')

        # Validate input fields
        if not order_id or not new_status:
            return Response(
                {"error": "Both 'order_id' and 'status' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if order exists
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate status choice
        allowed_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in allowed_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of: {', '.join(allowed_statuses)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update and save order status
        order.status = new_status
        order.save()

        return Response(
            {
                "message": "Order status updated successfully.",
                "order_id": order.id,
                "new_status": order.status,
            },
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
def order_status(request, order_id):
    """
    Retrieve the status of an order by ID.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=http_status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "order_id": order.id,
            "status": order.status  # Assuming your model has a 'status' field
        },
        status=http_status.HTTP_200_OK
    )