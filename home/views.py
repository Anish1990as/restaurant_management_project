from django.shortcuts import render, redirect
from django.conf import settings
from .models import Restaurant, MenuItem, Feedback
from .forms import Feedback


def home(request):
    restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Tasty Byte')
    phone_number = getattr(settings, 'RESTAURANT_PHONE', '+91 7880821765')
    return render(request, 'home/home.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number
    })

def home(request):
    menu_items = MenuItem.objects.all()
    return render(request, "home/home.html", {"menu_items": menu_items})


def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {'items': items})

def about(request):
    return render(request, 'home/aboutus.html')

def custom_404(request, exception):
    return render(request, 'home/404.html', status=404)

def contact(request):
    return render(request, 'home/contact.html')

def reservations(request):
    return render(request, 'home/reservations.html')

def feedback(request):
    return render(request, 'home/feedback.html')

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Feedback.objects.create(name=name, email=email, message=message)
        return redirect('feedback_thanks')
    return render(request, 'home/feedback.html')
    

def feedback_thanks(request):
      
    return render(request, 'home/feedback_thanks.html')

def search_menu(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = MenuItem.objects.filter(name__icontains=query)

    return render(request, "search_results.html", {"query": query, "results": results})

def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, "home/menu.html", {"menu_items": menu_items})
    
def menu_page(request):
    items = MenuItem.objects.all()  # sare menu items fetch kar lega
    return render(request, "home/menu.html", {"items": items})

def home(request):
    restaurant_info = RestaurantInfo.objects.first()
    return render(request, 'home/home.html', {'restaurant_info': restaurant_info})