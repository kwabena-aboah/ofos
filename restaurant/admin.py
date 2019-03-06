from django.contrib import admin

from . models import Food, Order


class FoodAdmin(admin.ModelAdmin):
	# Admin control over food
    list_display = ('id', 'food_name', 'food_details',
                    'price', 'active',)
    list_filter = ('food_name', 'price', 'active',)
    search_fields = ('food_name', 'price',)


admin.site.register(Food, FoodAdmin)


class OrderAdmin(admin.ModelAdmin):
	# Admin control over orders
    list_display = ('id', 'name', 'phone', 'address',
                    'delivery_date', 'food_id', 'payment_option',
                    'order_status', 'quantity', 'cash','order_date',)
    list_filter = ('name', 'delivery_date', 'order_status', 'order_date',)
    search_fields = ('name', 'delivery_date', 'food_id', 'order_status', 'order_date',)


admin.site.register(Order, OrderAdmin)
