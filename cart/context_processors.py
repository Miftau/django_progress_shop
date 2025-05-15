from .cart import Cart

# Create context_processor

def cart(request):
    # return cart default data
    return {'cart': Cart(request)}