

from django.contrib import admin
from Tshirtapp.views import *
from django.urls import path
urlpatterns = [
      path('',home,name='homepage'),
      path('cart',cart),
      path('orders',orders,name='orders'),
      path('login/',login),
      path('logout',logout),
      path('signup/',signup),
      path('checkout',checkout),
      path('product/<str:slug>',show_product),
      path('addtocart/<str:slug>/<str:size>',addtocart),
      path('validate_payment' , validatePayment)
     
      

      

]
