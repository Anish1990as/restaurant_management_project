from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import OrderStatus
from . import DEFAULT_STATUSES

@receiver(post_migrate)
def create_default_statuses(sender, **kwargs):
    if sender.name == "orders": 
        for status in DEFAULT_STATUSES:
            OrderStatus.objects.get_or_create(name=status)