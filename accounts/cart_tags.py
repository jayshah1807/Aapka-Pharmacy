from django import template
from math import floor
register = template.Library()

@register.simple_tag()
def multiply(a,b):
    # you would need to do any localization of the result here
    return int(a)*int(b)

# def add(x,y):
#     # you would need to do any localization of the result here
#     return x+y

@register.filter
def cal_total_payable_amount(item):
    total=0
    for key,values in item.items():
        price = values.product_price
        total+= price*int(key.quantity)
    return total