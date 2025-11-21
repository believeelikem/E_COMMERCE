from django.shortcuts import render
from .models import *
from django.http import JsonResponse

def store(request):
    order = Order.objects.get(customer = request.user.customer)
    
    total_items = order.cart_total_items
    products = Product.objects.all()  
    
    context = {
        "products":products,
        "total_items":total_items
    } 
    return render(request,"store/store.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer)
        
        items = order.items.all()
    else:
        class Ord:
            cart_total_items = 0
            cart_total_price = 0
        items = []
        order = Ord()
        
        # order = {"cart_total_items":0,"card_total_price":0}
    
    context = {
        "items":items,
        "cart_total_price" : order.cart_total_price,
        "cart_total_items":order.cart_total_items,
    }
    
    return render(request,"store/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer)
        
        items = order.items.all()
    else:
        class Ord:
            cart_total_items = 0
            cart_total_price = 0
        items = []
        order = Ord()
        
        # order = {"cart_total_items":0,"card_total_price":0}
    
    context = {
        "items":items,
        "cart_total_price" : order.cart_total_price,
        "cart_total_items":order.cart_total_items,
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
    order, created = Order.objects.get_or_create(customer = request.user.customer)
    print(order)
    
    order_item, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    print(order_item)
    print("before", order_item.quantity)
    if action == "add":
        order_item.quantity = order_item.quantity + 1
        order_item.save()
        print("after", order_item.quantity)
    elif action == "remove":
        order_item.quantity = order_item.quantity - 1
    
    if order_item.quantity <= 0:
        order_item.delete()
    
    return JsonResponse("Item was added", safe=False)

from django.http import HttpResponse

def update_count(request):
    order = Order.objects.get(customer = request.user.customer)
    
    total_items = order.cart_total_items
    
    return HttpResponse(f'{total_items}')
    
    