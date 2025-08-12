 from django.shortcuts import render
from django.conf import settings
from .models import Restaurant

def home(request):
    restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Tasty Byte')
    phone_number = getattr(settings, 'RESTAURANT_PHONE', '+91 7880821765')
    return render(request, 'home/home.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number
    })

def about(request):
    return render(request, 'home/aboutus.html')

def custom_404(request, exception):
    return render(request, 'home/404.html', status=404)

def menu_items(request):
    # Hardcoded menu items for now
    menu = [
        {"name": "Pizza Margherita", "price": 8.99},
        {"name": "Cheeseburger", "price": 6.49},
        {"name": "Pasta Alfredo", "price": 7.99},
        {"name": "French Fries", "price": 2.99},
    ]
    return render(request, "home/menu.html", {"menu": menu})

def contact(request):
    return render(request, 'home/contact.html')    