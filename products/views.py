from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer
from products.models import MenuItem


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
      
def menu_list(request):
    query = request.GET.get("q")
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)  # simple search
    else:
        menu_items = MenuItem.objects.all()

    return render(request, "products/menu.html", {"menu": menu_items, "query": query}) 

def menu_view(request):
    items = MenuItem.objects.all()
    return render(request, "products/menu.html", {"items": menu_items})


def product_list(request):
    breadcrumbs = [
        ("Home", "/"),
        ("Products", "/products/"),
    ]
    return render(request, "products/list.html", {"breadcrumbs": breadcrumbs})


def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})

    
    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1

    request.session['cart'] = cart
    return redirect('view_cart')


 
def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': item.price * quantity
        })
        total_price += item.price * quantity

    context = {
        'cart_items': items,
        'total_price': total_price
    }
    return render(request, 'cart/cart.html', context)


 
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('view_cart')