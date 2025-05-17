from django.shortcuts import render, get_object_or_404
from .cart import Cart
from progress_store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    return render(request, "cart_summary.html", {})


def cart_add(request):
    # Get the cart 
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        #Get data
        product_id = int(request.POST.get('product_id'))
        # Fetch product from DB
        product = get_object_or_404(Product, id=product_id)
        
        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Add product to session
        cart.add(product=product)
        #return JsonResponse({'product_name': product.name})
        return JsonResponse({'qty': cart_quantity})



def cart_delete(request):
    pass


def cart_update(request):
    pass
