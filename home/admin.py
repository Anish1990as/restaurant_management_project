from django.contrib import admin
from .models import Restaurant, MenuItem, Feedback, Order    


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")  
    search_fields = ("name",)  
    list_filter = ("price",)
    

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')

 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "menu_item", "quantity", "created_at")
    search_fields = ("customer_name",)
    list_filter = ("created_at",)
 