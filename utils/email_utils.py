from django.core.mail import send_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)

def send_order_confirmation_email(order_id, customer_email, customer_name=None, total_amount=None):
    """
    Sends an order confirmation email to the customer.
    """
    subject = f"Order Confirmation - #{order_id}"
    
    message = f"""
    Dear {customer_name or 'Customer'},
    
    Thank you for your order!
    Your order ID is: {order_id}.
    
    Total Amount: {total_amount if total_amount else 'N/A'}.

    We will notify you once your order is processed and shipped.
    
    Regards,
    Your Company Team
    """
    
    from_email = None  # Uses DEFAULT_FROM_EMAIL from settings

    try:
        send_mail(subject, message, from_email, [customer_email], fail_silently=False)
        return {"success": True, "message": f"Confirmation email sent to {customer_email}"}
    except BadHeaderError:
        logger.error("Invalid header found when sending order confirmation email.")
        return {"success": False, "message": "Invalid header found."}
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return {"success": False, "message": str(e)}