from django.contrib import admin
from django.urls import path,include
from . import views   
from .views import contact_view
from django.contrib.auth import views as auth_views
from .views import MenuCategoryListView
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet
from .views import MenuItemsByCategoryView
from .views import AvailableTablesAPIView


router = DefaultRouter()
router.register(r"menu-items", MenuItemViewSet, basename="menuitem")


urlpatterns = [
    path("admin/", admin.site.urls),    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('reservations/', views.reservations, name='reservations'),
    path("feedback/", views.feedback, name="feedback"),
    path('feedback/success/', views.feedback_success, name='feedback_success'),
    path("feedback_thanks/", views.feedback_thanks, name="feedback_thanks"),
    path('search/', views.search_menu, name='search_menu'),
    path("menu/", views.menu_list, name="menu_list"),  
    path("account/", include("account.urls")),
    path("menu/", views.menu_page, name="menu"),
    path("faq/", views.faq, name="faq"),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy')
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('place-order/', views.place_order, name='place_order'),
    path("menu-categories-list/", MenuCategoryListView.as_view(), name="menu-categories
    path("menu-items/by-category/", MenuItemsByCategoryView.as_view(), name="menu-items-by-category"),
    path("contact/submit/", ContactFormSubmissionView.as_view(), name="contact-form-submit"),
    path('api/tables/available/', AvailableTablesAPIView.as_view(), name='available_tables_api'),
]