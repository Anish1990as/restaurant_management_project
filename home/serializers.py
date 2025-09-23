from rest_framework import serializers
from products.models import MenuCategory    
from .models import MenuItem

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name'] 

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() 

    class Meta:
        model = MenuItem
        fields = ["id", "name", "price", "category"] 