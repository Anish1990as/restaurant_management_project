 from django.shortcuts import render
from django.conf import settings
from .models import Restaurant

def home(request):
    # Restaurant ka naam get karo
    if Restaurant.objects.exists():
        restaurant_name = Restaurant.objects.first().name
    else:
        restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Default Restaurant')

    return render(request, 'home.html', {
        'restaurant_name': restaurant_name
    })


def about(request):
    return render(request, 'about.html')


def homepage(request):
    return render(request, "home/index.html", {
        "phone_number": getattr(settings, 'RESTAURANT_PHONE', 'Not Available')
    })