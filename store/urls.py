from django.urls import path
from . import views 


urlpatterns = [
    path("",views.store,name = "store"),
    path("cart/",views.cart,name = "cart"),
    path("checkout/",views.checkout,name = "checkout"),
    path("update_item/",views.update_item,name = "update_item"),
    path("update-count/",views.update_count,name = "update_count"),
    path('process_order/', views.processOrder, name="process_order"),
]