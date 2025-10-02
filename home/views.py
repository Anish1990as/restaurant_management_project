from django.shortcuts import render, redirect
from django.conf import settings
from .models import Restaurant, MenuItem, Feedback
from .forms import Feedback
from django.utils import timezone
from products.models import TodaysSpecial, HomepageBanner
from .models import About
from .forms import FeedbackForm
from rest_framework.generics import ListAPIView
from products.models import MenuCategory
from .serializers import MenuCategorySerializer
from rest_framework import viewsets, filters, permissions
from .serializers import MenuItemSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import ContactFormSubmission
from .serializers import ContactFormSubmissionSerializer


class ContactFormSubmissionView(generics.CreateAPIView):
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact form submitted successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    items = MenuItem.objects.all()
    return render(request, "home/menu.html", {"items": items})

def home(request):
    restaurant_info = RestaurantInfo.objects.first()
    return render(request, 'home/home.html', {'restaurant_info': restaurant_info})

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks — we received your details.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, "home/contact.html", {"form": form})


def homepage(request):
    breadcrumbs = [
        ("Home", "/"),
    ]
    return render(request, "home/index.html", {"breadcrumbs": breadcrumbs})


def homepage(request):
    current_time = timezone.now()
    return render(request, "home/index.html", {"current_time": current_time})

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')

from django.shortcuts import render

def homepage(request):
    breadcrumbs = [
        {'title': 'Home', 'url': '/'},
    ]
    return render(request, 'home/homepage.html', {'breadcrumbs': breadcrumbs})

def menu_page(request):
    breadcrumbs = [
        {'title': 'Home', 'url': '/'},
        {'title': 'Menu', 'url': '/menu/'},
    ]
    return render(request, 'home/menu.html', {'breadcrumbs': breadcrumbs})

def order_confirmation(request):
    breadcrumbs = [
        {'title': 'Home', 'url': '/'},
        {'title': 'Orders', 'url': '/orders/'},
        {'title': 'Confirmation', 'url': '#'},
    ]
    return render(request, 'home/order_confirmation.html', {'breadcrumbs': breadcrumb

def place_order(request):
    return render(request, 'home/place_order.html')


def home(request):
    specials = TodaysSpecial.objects.all()
    banner = HomepageBanner.objects.first()  # ek banner hi use karenge
    return render(request, "home/home.html", {"specials": specials, "banner": banner})

def about_view(request):
    about = About.objects.first()
    return render(request, 'home/about.html', {'about': about})

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'home/feedback.html', {'form': form})


def feedback_success(request):
    return render(request, 'home/feedback_success.html')

class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class MenuItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
   
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class MenuItemViewSet(viewsets.ModelViewSet):
 
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    permission_classes = [permissions.IsAdminUser]


class MenuItemsByCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        category_name = request.query_params.get("category", None)

        if not category_name:
            return Response({"error": "Category parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        items = MenuItem.objects.filter(category__name__iexact=category_name)
        serializer = MenuItemSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)