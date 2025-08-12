from django.shortcuts import render
from django.conf import settings
from .models import Restaurant

def home(request):
    
    restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'My Restaurant')
    phone_number = getattr(settings, 'RESTAURANT_PHONE', '+91 0000000000')
    return render(request, 'home.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number
    

def about(request):
     
    return render(request, 'home/aboutus.html')

def custom_404(request, exception):
    
    return render(request, 'home/404.html', status=404)