from django.db import models
from django.contrib.auth.models import User
from products.models import Menu
from products.models import Product
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    # Managers
    objects = models.Manager()        # Default manager
    active = ActiveOrderManager()     # Custom manager

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_item_total(self):
        return self.quantity * self.menu_item.price


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})" 


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
        
        
class Order(models.Model):
    customer_name = models.CharField(max_length=100)   # example field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New status field
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} ({self.status})"

# Custom Manager
class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        return self.filter(status__in=['pending', 'processing'])