from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets, filters, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.email_utils import send_email

from .models import (
    Restaurant,
    MenuItem,
    Feedback,
    About,
    ContactFormSubmission,
    RestaurantInfo,
)
from .forms import FeedbackForm, ContactForm
from products.models import TodaysSpecial, HomepageBanner, MenuCategory
from .serializers import (
    MenuCategorySerializer,
    MenuItemSerializer,
    ContactFormSubmissionSerializer,
)


class ContactFormSubmissionView(CreateAPIView):
    queryset = ContactFormSubmission.objects.all()
    serializer_class = ContactFormSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact form submitted successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

def home(request):
    specials = TodaysSpecial.objects.all()
    banner = HomepageBanner.objects.first()
    restaurant_info = RestaurantInfo.objects.first()
    return render(
        request,
        "home/home.html",
        {"specials": specials, "banner": banner, "restaurant_info": restaurant_info},
    )


def about_view(request):
    about = About.objects.first()
    return render(request, "home/about.html", {"about": about})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks — we received your details.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "home/contact.html", {"form": form})


def reservations(request):
    return render(request, "home/reservations.html")


def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("feedback_success")
    else:
        form = FeedbackForm()
    return render(request, "home/feedback.html", {"form": form})


def feedback_success(request):
    return render(request, "home/feedback_success.html")


def search_menu(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = MenuItem.objects.filter(name__icontains=query)
    return render(request, "search_results.html", {"query": query, "results": results})


def menu_page(request):
    items = MenuItem.objects.all()
    return render(request, "home/menu.html", {"items": items})


def custom_404(request, exception):
    return render(request, "home/404.html", status=404)


def privacy_policy(request):
    return render(request, "home/privacy_policy.html")


def order_confirmation(request):
    breadcrumbs = [
        {"title": "Home", "url": "/"},
        {"title": "Orders", "url": "/orders/"},
        {"title": "Confirmation", "url": "#"},
    ]
    return render(request, "home/order_confirmation.html", {"breadcrumbs": breadcrumbs})


def place_order(request):
    return render(request, "home/place_order.html")


 
class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class MenuItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
 
    pagination_class = MenuItemPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    
    permission_classes = [permissions.IsAdminUser]


class MenuItemsByCategoryView(APIView):
    def get(self, request, *args, **kwargs):
        category_name = request.query_params.get("category", None)
        if not category_name:
            return Response(
                {"error": "Category parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items = MenuItem.objects.filter(category__name__iexact=category_name)
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Call utility function
            send_email(
                recipient_email=submission.email,
                subject="Thanks for contacting us!",
                message_body=f"Hi {submission.name},\n\nWe received your message:\n\n{submission.message}\n\nOur team will reply soon.\n\nBest,\nTasty Byte",
            )

            messages.success(request, "Thanks — we received your details.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "home/contact.html", {"form": form})
