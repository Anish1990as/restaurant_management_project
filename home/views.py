from django.shortcuts import render

# Create your views here.
from django.conf import settings
from .models import Restaurant

def home(request):

    if Restaurant.objects.exists():
     restaurent_name = Restaurant.objects.first().name 
    else:
        restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Restaurant Name')

    return render(request, 'home.html',{'restaurent_name': restaurent_name})