

from django.contrib import admin
from Tshirtapp.views import *
from django.urls import path
urlpatterns = [
      path('',home,name='homepage'),
      path('cart/',cart),
      path('order/',order),
      path('login/',login),
      path('logout/',logout),
      path('signup/',signup),
      path('checkout/',checkout),
      path('product/<str:slug>',show_product),
      path('addtocart/<str:slug>/<str:size>',addtocart)
      

      

]
