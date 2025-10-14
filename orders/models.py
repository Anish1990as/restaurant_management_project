from django.db import models
from decimal import Decimal
from account.models import CustomUser
from home.models import MenuItem
from products.models import Product
from .utils import generate_unique_order_id
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
 
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
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
        

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.00 = 10%
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"

    @property
    def is_valid(self):
        """Check if the coupon is active and within date range."""
        today = timezone.now().date()
        return self.is_active and self.valid_from <= today <= self.valid_until


 def calculate_total(self, save=False):
        """
        Calculate total price for this order by summing all order item line totals,
        applying per-line or global discounts using calculate_discount (if available).

        Args:
            save (bool): If True, update self.total_price and save the Order.

        Returns:
            Decimal: total price rounded to 2 decimal places.
        """
        # Avoid floating point issues
        total = Decimal('0.00')

        # Try to import calculate_discount utility. If not present, set fallback.
        try:
            from .utils import calculate_discount
        except Exception:
            calculate_discount = None

        # Expecting an OrderItem relation. Common names are order.items, order.order_items, etc.
        # Adjust the related_name below if your OrderItem uses a different related_name.
        # We'll try a few common names for robustness.
        possible_related_names = ['items', 'order_items', 'orderitem_set']

        order_items_qs = None
        for rel in possible_related_names:
            if hasattr(self, rel):
                order_items_qs = getattr(self, rel).all()
                break

        # If still None, try to inspect related objects (fallback)
        if order_items_qs is None:
            # Fallback: try reverse relation (single related manager)
            # This will raise if there are none; we'll treat as no items.
            try:
                order_items_qs = self.orderitem_set.all()
            except Exception:
                order_items_qs = []

        # Iterate through items and build total
        for item in order_items_qs:
            # Attempt to find price and qty on the item
            # Common field names: price, unit_price, product.price
            qty = getattr(item, 'quantity', None)
            if qty is None:
                qty = getattr(item, 'qty', 1) or 1
            try:
                qty = int(qty)
            except Exception:
                qty = 1

            # Price resolution
            price = getattr(item, 'price', None)
            if price is None:
                # Try item.unit_price
                price = getattr(item, 'unit_price', None)
            if price is None:
                # Try product related field: item.product.price
                product = getattr(item, 'product', None)
                if product is not None:
                    price = getattr(product, 'price', None)

            # If price still None, skip this item
            if price is None:
                continue

            # Ensure Decimal
            line_price = Decimal(price)
            line_total = (line_price * Decimal(qty))

            # Apply discount via calculate_discount if available
            if callable(calculate_discount):
                try:
                    # calculate_discount can accept (order, item, line_total) or (line_total,)
                    # We'll call it with (self, item, line_total) first and fallback.
                    discount_amount = calculate_discount(self, item, line_total)
                except TypeError:
                    try:
                        discount_amount = calculate_discount(line_total)
                    except Exception:
                        discount_amount = Decimal('0.00')
                except Exception:
                    discount_amount = Decimal('0.00')

                # Ensure decimal
                if discount_amount is None:
                    discount_amount = Decimal('0.00')
                else:
                    discount_amount = Decimal(discount_amount)
                # Prevent negative totals
                if discount_amount < 0:
                    discount_amount = Decimal('0.00')

                line_total = line_total - discount_amount

            total += line_total

        # Round to 2 decimal places
        total = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if save:
            self.total_price = total
            self.save(update_fields=['total_price'])

        return total