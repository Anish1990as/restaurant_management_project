import string
import secrets
from .models import Coupon
from .models import Order

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