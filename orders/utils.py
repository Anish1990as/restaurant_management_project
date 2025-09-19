import string
import secrets
from .models import Coupon

def generate_coupon_code(length=10):
    """Generate a unique alphanumeric coupon code."""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(length))

    # ensure uniqueness
    while Coupon.objects.filter(code=code).exists():
        code = ''.join(secrets.choice(characters) for _ in range(length))

    return code