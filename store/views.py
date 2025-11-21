from django.shortcuts import render
from .models import *

def store(request):
    products = Product.objects.all()  
    
    context = {
        "products":products
    } 
    return render(request,"store/store.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer)
        
        items = order.items.all()
    else:
        items = []
        order = {"cart_total_items":0,"card_total_price":0}
    
    context = {
        "items":items,
        "cart_total_price" : order.cart_total,
        "cart_total_items":order.cart_total_items
    }
    
    return render(request,"store/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer)
        
        items = order.items.all()
    else:
        items = []
        order = {"cart_total_items":0,"card_total":0}
    
    context = {
        "items":items,
        "cart_total_price" : order.cart_total,
        "cart_total_items":order.cart_total_items
    }    
    return render(request,"store/checkout.html",context)