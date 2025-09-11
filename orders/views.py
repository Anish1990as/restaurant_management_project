from django.shortcuts import render
import random
# Create your views here.

def order_confirmation(request):
    # Generate a sample order number (you can replace this with actual order id from DB)
    order_number = random.randint(10000, 99999)
    context = {
        'order_number': order_number
    }
    return render(request, 'orders/order_confirmation.html', context)
