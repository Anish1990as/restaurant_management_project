from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer

'''
NOTE: Conside this as a reference and follow this same coding structure or format to work on you tasks
'''

class ItemAPIView(APIView):

    def get(self, request):
       
        try:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
      
class MenuView(APIView):
    def get(self, request):
        menu = [
            {"name": "Margherita Pizza", "description": "Classic cheese and tomato pizza", "price": 299},
            {"name": "Paneer Butter Masala", "description": "Cottage cheese in rich tomato gravy", "price": 349},
            {"name": "Veg Biryani", "description": "Fragrant basmati rice with vegetables", "price": 279},
            {"name": "Gulab Jamun", "description": "Sweet fried dumplings soaked in sugar syrup", "price": 99},
        ]
        return Response(menu)