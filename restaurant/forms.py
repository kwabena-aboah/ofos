from django.forms import ModelForm
from django import forms
from . models import Order, Food


class OrderForm(ModelForm):
    OPTIONS = (
        ('Postpay', 'Postpay'),
        ('Prepay', 'Prepay')
    )

    OPTIONS2 = (
        ('Confirm', 'Confirm'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    order_status = forms.TypedChoiceField(
        required=False, choices=OPTIONS2, widget=forms.RadioSelect)
    payment_option = forms.ChoiceField(choices=OPTIONS)
    food_id = forms.ModelChoiceField(
        queryset=Food.objects.filter(active='1'))
    delivery_date = forms.DateField(required=True)
    quantity = forms.IntegerField(initial=1)
    cash = forms.DecimalField(required=True)
    order_date = forms.DateField(required=True)

    class Meta:
        model = Order
        fields = ['name', 'phone', 'address', 'delivery_date',
                  'food_id', 'payment_option', 'order_status','quantity', 'cash','order_date']


class FoodForm(ModelForm):
	class Meta:
		model = Food
		fields = ['food_name', 'food_details', 'price','vat']         