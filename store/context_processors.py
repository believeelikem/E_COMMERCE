from .models import *

def total_items(request):
    order = Order.objects.get(customer = request.user.customer)
    
    total_items = order.cart_total_items 
    return {
        "total_items":total_items
    }