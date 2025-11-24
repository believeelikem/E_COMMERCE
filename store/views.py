from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .utils import cookieCart,cartData


def store(request):
    data = cartData(request)   
    order = data["order"]
    
    products = Product.objects.all()  
    
    context = {
        "products":products,
        "cart_total_price" : order.cart_total_price,
        "cart_total_items":order.cart_total_items,
        "shipping": order.shipping
    } 
    
    return render(request,"store/store.html",context)

def cart(request):
    data = cartData(request)   
    order = data["order"]
    items = data["items"]

    context = {
        "items":items,
        "cart_total_price" : order.cart_total_price,
        "cart_total_items":order.cart_total_items,
        "shipping": order.shipping
    }

    return render(request,"store/cart.html",context)

def checkout(request):
    data = cartData(request)   
    order = data["order"]
    items = data["items"]
    
    context = {
        'order':order,
        "items":items,
        "cart_total_price" : order.cart_total_price,
        "cart_total_items":order.cart_total_items,
        "shipping": order.shipping

    }
    return render(request,"store/checkout.html",context)

import json
def update_item(request):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    print(data)
    
    product = Product.objects.get(id = product_id)
    print(product)
    order, created = Order.objects.get_or_create(customer = request.user.customer,complete = False)
    print(order)
    
    order_item, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    print(order_item)
    print("before", order_item.quantity)
    if action == "add":
        order_item.quantity = order_item.quantity + 1
        print("after", order_item.quantity)
    elif action == "remove":
        order_item.quantity = order_item.quantity - 1
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()
    
    return JsonResponse("Item was added", safe=False)

from django.http import HttpResponse

def update_count(request):
    ...
    # order,created  = Order.objects.get(customer = request.user.customer)
    
    # total_items = order.cart_total_items
    
    # return HttpResponse(f'{total_items}')
  
import datetime  
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer = request.user.customer,complete = False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id
        
        if total == order.cart_total_price:
            
            print(total == order.cart_total_items)
            order.complete = True
            order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = request.user.customer,
                address = data["shipping"]["address"],
                city = data["shipping"]["city"],
                state = data["shipping"]["zipcode"],
            )

    else:
        print("User is not logged in ")
    return JsonResponse('Payment submitted..', safe=False)
