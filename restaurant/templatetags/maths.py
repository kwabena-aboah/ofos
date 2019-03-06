from django import template

from restaurant.models import Order


register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
	"""Performs subtraction"""
	return float(value - arg)

@register.filter(name='multiply')
def multiply(value, arg):
	return float(value * arg)

@register.filter(name='addition')
def addition(value, arg):
	return float(value + arg)
