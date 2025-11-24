import json
from .models import *

def cookieCart(request):
        try:
            cart = json.loads(request.COOKIES["cart"])
            print(cart)
        except:
            cart = {}

        class Ord:
            cart_total_items = 0
            cart_total_price = 0
            shipping = False
            
        items = []
        order = Ord()
            
        cart_total_items = 0
        for i in cart:
            try:
                cart_total_items += cart[i]["quantity"]
                product = Product.objects.get(id = i)
                
                total = product.price * cart[i]["quantity"]
                order.cart_total_price += total
                
                item = {
                    'product':{
                    'id':product.id,
                    'name':product.name, 
                    'price':product.price, 
                    'image':{"url":product.image.url}
                }, 
                'quantity':cart[i]['quantity'],
                'get_total':total,
                    
                }
                items.append(item)
                
                if not product.digital:
                    order.shipping = True
            except:
                pass
    
        order.cart_total_items = cart_total_items
        
        return {"order":order,"items":items}
    
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        
        items = order.items.all()
    else:
        cookie_data = cookieCart(request)
        order = cookie_data["order"]
        items = cookie_data["items"]
        
    return {"order":order,"items":items}    