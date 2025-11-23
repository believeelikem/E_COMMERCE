from .models import *

def total_items(request):
    if request.user.is_authenticated:
        order = Order.objects.get_or_create(customer = request.user.customer)
        total_items = order.cart_total_items 
    else:
        total_items = 0
    
    total_items =  total_items
    return {
        "total_items":total_items
    }