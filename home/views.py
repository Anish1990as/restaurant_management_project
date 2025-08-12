from django.shortcuts import render
from django.conf import settings
from .models import Restaurant

def home(request):
    """Homepage View"""
    # Restaurant ka naam get karo
    if Restaurant.objects.exists():
        restaurant_name = Restaurant.objects.first().name
    else:
        restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Default Restaurant')

    phone_number = getattr(settings, 'RESTAURANT_PHONE', 'Not Available')

    return render(request, 'home/home.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number
    })

def about(request):
    """About Us Page"""
    return render(request, 'home/aboutus.html')

def custom_404(request, exception):
    """Custom 404 Page"""
    return render(request, 'home/404.html', status=404)