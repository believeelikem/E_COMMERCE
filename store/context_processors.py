from .models import *
import json

def total_items(request):
    if request.user.is_authenticated:
        order,_ = Order.objects.get_or_create(customer = request.user.customer,complete = False)
        total_items = order.cart_total_items 
    else:
        try:
            cart = json.loads(request.COOKIES["cart"])
            print(cart)
        except:
            cart = {}
        cart_total_items = 0
        for i in cart:
            cart_total_items += cart[i]["quantity"]
        total_items = cart_total_items
    
    total_items =  total_items
    return {
        "total_items":total_items
    }