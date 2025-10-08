import string
import secrets
from .models import Coupon
from .models import Order
from django.db.models import Sum


def generate_coupon_code(length=10):
    """Generate a unique alphanumeric coupon code."""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))

    # ensure uniqueness
    while Coupon.objects.filter(code=code).exists():
        code = ''.join(secrets.choice(characters) for _ in range(length))

    return code


def generate_unique_order_id(length=8):
    """
    Generate a unique alphanumeric ID for an Order.
    Uses the secrets module for cryptographically secure random generation.
    """
    characters = string.ascii_uppercase + string.digits  # e.g. A-Z, 0-9
    while True:
        order_id = ''.join(secrets.choice(characters) for _ in range(length))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id

    
def get_daily_sales_total(date):
    """
    Calculate the total sales for a specific date.
    Args:
        date (datetime.date): The date for which to calculate total sales.
    Returns:
        Decimal: Total sales amount for the given date, or 0 if no orders exist.
    """
    orders = Order.objects.filter(created_at__date=date)
    total = orders.aggregate(total_sum=Sum('total_price'))['total_sum']
    return total or 0