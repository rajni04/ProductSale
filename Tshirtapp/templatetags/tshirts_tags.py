from django import template
register = template.Library()
from math import floor



@register.filter
def rupee(number):
    return f'₹{number}'
@register.simple_tag
def min_price(t):
    print(min_price)
    size=t.sizevariant_set.all().order_by('price').first()
    return floor(size.price)

@register.simple_tag
def sale_price(t):
    price=min_price(tshirt)
    discount=t.discount
    return floor(price - (price *(discount/100)))

@register.simple_tag
def get_active_button(active_size,size):
    print(active_size,size)
    if active_size == size:
        return "success"
    return "light"


@register.simple_tag
def multiply(a,b):

    return a*b

@register.simple_tag
def cal_selprice(price,discount):

    return floor(price - (price *(discount/100)))

@register.filter
def cal_total_payable_amount(cart):
    total=0
    for c in cart:
        discount=c.get('tshirt').discount
        price=c.get('size').price
        sale_price=cal_selprice(price,discount)
        total_of_single_pro=sale_price* c.get('quantity')
        total=total+total_of_single_pro
    return total