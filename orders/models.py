from django.db import models
from decimal import Decimal
from account.models import CustomUser
from home.models import MenuItem
from products.models import Product
from .utils import generate_unique_order_id

 
class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        return self.filter(status__in=['pending', 'processing'])


 
class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


 
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    order_id = models.CharField(max_length=12, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

     
    objects = models.Manager()       
    active = ActiveOrderManager()    

    def save(self, *args, **kwargs):
        if not self.order_id:   
            self.order_id = generate_unique_order_id()
        super().save(*args, **kwargs)

    def calculate_total(self):
        total = Decimal('0.00')
        for item in self.items.all():   
            total += item.price * item.quantity
        self.total_amount = total
        return total

    def __str__(self):
        return f"Order {self.order_id} - {self.customer}"


 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


 
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"