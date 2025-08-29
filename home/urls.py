from django.contrib import admin
from django.urls import path
from . import views   

urlpatterns = [
    path("admin/", admin.site.urls),    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('reservations/', views.reservations, name='reservations'),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback_thanks/", views.feedback_thanks, name="feedback_thanks"),
    path('search/', views.search_menu, name='search_menu'),
    path("menu/", views.menu_list, name="menu_list"),  
    path("account/", include("account.urls")),   
    path("menu/", views.menu_page, name="menu"),
]
 