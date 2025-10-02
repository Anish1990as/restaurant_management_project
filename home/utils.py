from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_email(recipient_email, subject, message_body, from_email=None):
    """
    Reusable function to send emails.
    Args:
        recipient_email (str/list): Single email string or list of recipient emails
        subject (str): Subject of the email
        message_body (str): Body of the email
        from_email (str, optional): Sender email (defaults to settings.DEFAULT_FROM_EMAIL)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    if from_email is None:
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

    try:
        if not recipient_email:
            raise ValueError("Recipient email is required")

        # send_mail automatically handles lists or single strings
        send_mail(
            subject,
            message_body,
            from_email,
            [recipient_email] if isinstance(recipient_email, str) else recipient_email,
            fail_silently=False,
        )
        return True
    except BadHeaderError:
        logger.error("Invalid header found while sending email.")
        return False
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False