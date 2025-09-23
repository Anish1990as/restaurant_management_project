from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging

logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    """
    Validate an email address using Django's built-in validator.
    Returns True if valid, False otherwise.
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        logger.warning(f"Invalid email attempted: {email}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while validating email: {str(e)}")
        return False