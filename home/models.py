 from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default="Anonymous")
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    

class Order(models.Model):   
    customer_name = models.CharField(max_length=100)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.menu_item.name} x{self.quantity})"

 
class Order(models.Model):
    menu_item = models.ForeignKey(
        'MenuItem',
        on_delete=models.CASCADE,
        related_name="home_orders"    
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
 
 
 
