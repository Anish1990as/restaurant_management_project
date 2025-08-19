from django.shortcuts import render, redirect
from django.conf import settings
from .models import Restaurant, MenuItem, Feedback
from .forms import FeedbackForm


def home(request):
    restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Tasty Byte')
    phone_number = getattr(settings, 'RESTAURANT_PHONE', '+91 7880821765')
    return render(request, 'home/home.html', {
        'restaurant_name': restaurant_name,
        'phone_number': phone_number
    })

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


def menu_items(request):
     
    menu = [
         {"name": "Garlic Bread", "price": 3.99, "image": "https://source.unsplash.com/200x150/?garlic-bread"},
        {"name": "Spring Rolls", "price": 4.49, "image": "https://source.unsplash.com/200x150/?spring-rolls"},
        {"name": "Tomato Soup", "price": 2.99, "image": "https://source.unsplash.com/200x150/?tomato-soup"},

        # Main Course
        {"name": "Pizza Margherita", "price": 8.99, "image": "https://source.unsplash.com/200x150/?pizza"},
        {"name": "Cheeseburger", "price": 6.49, "image": "https://source.unsplash.com/200x150/?burger"},
        {"name": "Pasta Alfredo", "price": 7.99, "image": "https://source.unsplash.com/200x150/?pasta"},
        {"name": "Grilled Chicken", "price": 10.99, "image": "https://source.unsplash.com/200x150/?grilled-chicken"},
        {"name": "Paneer Butter Masala", "price": 9.49, "image": "https://source.unsplash.com/200x150/?paneer"},

        # Desserts
        {"name": "Chocolate Lava Cake", "price": 5.49, "image": "https://source.unsplash.com/200x150/?chocolate-cake"},
        {"name": "Gulab Jamun", "price": 3.49, "image": "https://source.unsplash.com/200x150/?gulab-jamun"},
        {"name": "Cheesecake", "price": 6.99, "image": "https://source.unsplash.com/200x150/?cheesecake"},

        # Drinks
        {"name": "Fresh Lime Soda", "price": 1.99, "image": "https://source.unsplash.com/200x150/?lime-soda"},
        {"name": "Cold Coffee", "price": 2.99, "image": "https://source.unsplash.com/200x150/?cold-coffee"},
        {"name": "Mango Smoothie", "price": 3.99, "image": "https://source.unsplash.com/200x150/?mango-smoothie"},
    ]
    return render(request, "home/menu.html", {"menu": menu})

 