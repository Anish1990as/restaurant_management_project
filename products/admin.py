from django.contrib import admin
from .models import *
from .models import TodaysSpecial


class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name','item_price','created_at']
 
admin.site.register(Item,ItemAdmin,Menu)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'image')


@admin.register(TodaysSpecial)
class TodaysSpecialAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name',)