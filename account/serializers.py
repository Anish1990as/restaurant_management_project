from rest_framework import serializers
from .models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']  # fields user can update
        read_only_fields = ['id', 'is_verified']        # prevent editing system fields