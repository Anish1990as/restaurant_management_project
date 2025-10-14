import string
import secrets
from .models import Coupon
from .models import Order
from django.db.models import Sum
from decimal import Decimal

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


def calculate_discount(order, item=None, line_total=None):
    """
    Example discount calculator.
    - If order has a coupon attribute and coupon.discount_percentage, apply percentage on line_total.
    - Otherwise return Decimal('0.00').

    This is intentionally simple — adjust to your business logic.
    """
    if line_total is None:
        return Decimal('0.00')

    # Example: if Order has attribute 'coupon' (FK to Coupon), apply its discount_percentage
    coupon = getattr(order, 'coupon', None)
    if coupon and getattr(coupon, 'is_active', False):
        try:
            pct = Decimal(getattr(coupon, 'discount_percentage', 0))
            # if stored as 10 for 10%, convert to fraction if needed
            if pct > 1:
                pct = pct / Decimal('100')
            discount_amount = (Decimal(line_total) * pct).quantize(Decimal('0.01'))
            return discount_amount
        except Exception:
            return Decimal('0.00')

    # No discount
    return Decimal('0.00')