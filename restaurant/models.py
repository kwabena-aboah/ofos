from django.db import models


class Food(models.Model):
    """Defines table for handling products."""
    food_name = models.CharField(max_length=200)
    food_details = models.TextField()
    price = models.FloatField(default="2.00")
    vat = models.FloatField(default='0.36')
    active = models.IntegerField(default='1')

    def __str__(self):
        return '%s (%s GH¢)' % (self.food_name, self.price)


class Order(models.Model):
	"""Defines table for customer food orders."""
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=11)
	address = models.TextField()
	delivery_date = models.DateField(blank=True)
	food_id = models.ForeignKey(Food, on_delete=models.CASCADE,)
	payment_option = models.CharField(max_length=50)
	order_status = models.CharField(max_length=50)
	quantity = models.IntegerField()
	cash = models.FloatField(default='0.00')
	order_date = models.DateField(auto_now_add=False, help_text='Date order was made')