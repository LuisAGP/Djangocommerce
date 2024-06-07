from django import template

register = template.Library()

@register.filter(name='money_format')
def money_format(value):
    return "${:,.2f}".format(value)


@register.filter(name='times') 
def times(number):
    return range(1,number+1)


@register.filter(name='filter_text') 
def filter_text(text):
    return str(text).replace("<br/>", "\n")


@register.simple_tag
def multiply(n1, n2, **kwargs):
    return n1*n2