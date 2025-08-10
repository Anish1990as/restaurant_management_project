from django.shortcuts import render

# Create your views here.
from django.conf import settings
from .models import Restaurant

def home(request):
    restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Default Restaurant')

    return render(request, 'home.html',{'restaurent_name': restaurent_name})