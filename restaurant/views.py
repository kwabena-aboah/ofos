from django.shortcuts import render, redirect
from django.urls import reverse
from . models import Order, Food
from . forms import OrderForm, FoodForm
from Project.search import get_query
from django.contrib import messages
from django.contrib.auth. decorators import login_required


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
    return render(request, 'restaurant/show.html', context)


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
    foods = Food.objects.filter(active='1')
    context = {'foods': foods}
    return render(request, 'restaurant/foods.html', context)


@login_required
def new_food(request):
    """Create new food in system"""
    if request.POST:
        form = FoodForm(request.POST)
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


# @login_required
# def general_report(request, order_date):
#     """Yearly reports on sales order"""
#     orders = Order.objects.get(order_date=order_date)
#     count_year = orders.count()
#     total = (orders.food_id.price + orders.quantity) + orders.food_id.vat
#     year_total = sum(total)
#     while True:
#         if count_year == 'True':
#             return year_total
#         else:
#             return render('/general_report', messages.error('No reports for this year', 'alert-danger'))

#     context = {"orders": orders, "count_year": count_year, "year_total": year_total }
#     return render(request, 'restaurant/reports.html', context)


# @login_required
# def search(request):
#     query_string = ''
#     found_order = None
#     if ('q' in request.GET) and request.GET['q'].strip():
#         query_string = request.GET['q']
#         order = get_query(query_string,
#                     ['name', 'delivery_date', 'food_id', 'order_status', 'order_date'])
#         found_order = Order.objects.filter(order).order_by('-order_date')
#     context = {'query_string': query_string, 'found_order': found_order}
#     return render(request, 'restaurant/search.html', context)