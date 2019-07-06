from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import Order, Food
from . forms import OrderForm, FoodForm
from django.views.generic import View

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response


@login_required
def index(request):
    """Lists all orders at homePage"""
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'restaurant/index.html', context)

@login_required
def show(request, order_id):
    """display details of an order"""
    order = Order.objects.filter(id=order_id)
    context = {'order': order}
    return render(request, 'restaurant/print.html', context)

@login_required
def new_order(request):
    """Create new Order for food"""
    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            if form.save():
                return redirect('/', messages.success(request, 'Successfully created Order.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Could not save data', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form not valid', 'alert-danger'))
    else:
        form = OrderForm()
        context = {'form': form}
        return render(request, 'restaurant/new.html', context)

@login_required
def edit_order(request, order_id):
    """Update Order form for food"""
    order = Order.objects.get(id=order_id)
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if form.save():
                return redirect('/', messages.success(request, 'Successfully updated order.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Could not update order.', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form not valid', 'alert-danger'))
    else:
        form = OrderForm(instance=order)
        context = {'form': form}
        return render(request, 'restaurant/edit.html', context)

@login_required
def delete_order(request, order_id):
    """Deletes an order"""
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('/', messages.success(request, 'Successfully deleted order', 'alert-success'))

@login_required
def foods(request):
    """List all active foods"""
    foods = Food.objects.all()
    context = {'foods': foods}
    return render(request, 'restaurant/foods.html', context)

@login_required
def new_food(request):
    """Create new food in system"""
    if request.POST:
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save():
                return redirect('/foods', messages.success(request, 'Successfully created new food', 'alert-success'))
            else:
                return redirect('/foods', messages.error(request, 'Data not saved', 'alert-danger'))
        else:
            return redirect('/foods', messages.error(request, 'Form not valid', 'alert-danger'))
    else:
        food_form = FoodForm()
        context = {'food_form': food_form}
        return render(request, 'restaurant/new_food.html', context)

@login_required
def delete_food(request, food_id):
    """Deletes a specific food"""
    if Food.objects.filter(id=food_id).update(active='0'):
        return redirect('/foods', messages.success(request, "Food was successfully deleted", "alert-success"))
    else:
        return redirect('/foods', messages.error(request, 'Cannot delete food', 'alert-danger'))


class ReportView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'restaurant/reports.html')

def general_report(request, *args, **kwargs):
    data = {
        "orders": 100,
        "foods": 10,
    }
    return JsonResponse(data)

User = get_user_model()

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        user_count = User.objects.all().count()
        food_count = Food.objects.all().count()
        order_count = Order.objects.all().count()
        labels = ['Users', 'Foods', 'Orders']
        default_items = [user_count, food_count, order_count]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)
