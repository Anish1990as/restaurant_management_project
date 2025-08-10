from django.shortcuts import render

# Create your views here.
from django.conf import settings
from .models import Restaurant

def home(request):

    if Restaurant.objects.exists():
        restaurant_name = Restaurant.objects.first().name 
    else:
        restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Default Restaurant')

    return render(request, 'home.html',{'restaurant_name': restaurant_name})