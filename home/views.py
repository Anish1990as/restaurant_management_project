from django.shortcuts import render

# Create your views here.
from django.conf import settings

def home(request):
    restaurent_name = settings.RESTAURENT_NAME 
    return render(request, 'home.html',{'restaurent_name': restaurent_name})