from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from .models import Order
from .models import Coupon

class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    item_price = serializers.DecimalField(source="item.price", max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "item_name", "item_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "total_price", "items"]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'username', 'order_date', '
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "order_id", "customer", "status", "created_at"]
        read_only_fields = ["id", "order_id", "customer", "created_at"]


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'is_active', 'valid_from', 'valid_until']


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        allowed_statuses = ['pending', 'processing', 'completed', 'cancelled']
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of: {', '.join(allowed_statuses)}.")
        return value
