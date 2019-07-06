import datetime
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Budget, BudgetEstimate
from categories.models import Category
from transactions.models import Transaction
from .forms import BudgetEstimateForm, BudgetForm


def dashboard(request):
    """
    Provides a high-level rundown of recent activity and budget status.
    """
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_year, end_month = today.year, today.month + 1

    if end_month > 12:
        end_year += 1
        end_month = 1

    end_date = datetime.date(end_year, end_month, 1) - datetime.timedelta(days=1)

    try:
        budget = Budget.active.get_queryset(datetime.datetime.today())
    except ObjectDoesNotExist:
        # Since there are no budgets at this point, pass them on to setup
        # as this view is meaningless without at least basic data in place.
        return HttpResponseRedirect(reverse('budget:budget_setup'))

    latest_expenses = Transaction.expenses.get_latest()
    latest_incomes = Transaction.incomes.get_latest()

    estimated_amount = budget.monthly_estimated_total()
    amount_used = budget.actual_total(start_date, end_date)

    if estimated_amount == 0:
        progress_bar_percent = 100
    else:
        progress_bar_percent = int(amount_used / estimated_amount * 100)

    if progress_bar_percent >= 100:
        progress_bar_percent = 100
    context = {
        'budget': budget,
        'latest_expenses': latest_expenses,
        'latest_incomes': latest_incomes,
        'estimated_amount': estimated_amount,
        'amount_used': amount_used,
        'progress_bar_percent': progress_bar_percent,
    }
    return render(request, 'dashboard.html', context)


def setup(request):
    """
    Displays a setup page which ties together the
    category/budget/budget estimate areas with explanatory text on how to use
    to set everything up properly.
    """
    return render(request, 'setup.html')


def summary_list(request):
    """
    Displays a list of all months that may have transactions for that month.
    """
    dates = Transaction.active.all().dates('date', 'month')
    context = {'dates': dates}
    return render(request, 'summaries/summary_list.html', context)


def summary_year(request, year):
    """
    Displays a budget report for the year to date.
    """
    start_date = datetime.date(int(year), 1, 1)
    end_date = datetime.date(int(year), 12, 31)
    budget = Budget.active.get_queryset(end_date)
    estimates_and_transactions, actual_total = budget.estimates_and_transactions(start_date, end_date)
    context = {
        'budget': budget,
        'estimates_and_transactions': estimates_and_transactions,
        'actual_total': actual_total,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'summaries/summary_year.html', context)


def summary_month(request, year, month):
    """
    Displays a budget report for the month to date.
    """
    start_date = datetime.date(int(year), int(month), 1)
    end_year, end_month = int(year), int(month) + 1

    if end_month > 12:
        end_year += 1
        end_month = 1

    end_date = datetime.date(end_year, end_month, 1) - datetime.timedelta(days=1)
    budget = Budget.active.get_queryset(end_date)
    estimates_and_transactions, actual_total = budget.estimates_and_transactions(start_date, end_date)
    context = {
        'budget': budget,
        'estimates_and_transactions': estimates_and_transactions,
        'actual_total': actual_total,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'summaries/summary_month.html', context)


def budget_list(request):
    """
    A list of budget objects.
    """
    budgets_list = Budget.active.all()
    try:
        paginator = Paginator(budgets_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        budgets = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    context = {
        'budgets': budgets,
        'paginator': paginator,
        'page': page,
    }
    return render(request, 'budgets/list.html', context)


def budget_add(request):
    """
    Create a new budget object.
    """
    if request.POST:
        form = BudgetForm(request.POST)

        if form.is_valid():
            budget = form.save()
            return HttpResponseRedirect(reverse('budget:budget_budget_list'))
    else:
        form = BudgetForm()
    context = {'form': form}
    return render(request, 'budgets/add.html', context)


def budget_edit(request, slug):
    """
    Edit a budget object.
    """
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    if request.POST:
        form = BudgetForm(request.POST, instance=budget)

        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget:budget_budget_list'))
    else:
        form = BudgetForm(instance=budget)
    context = {'budget': budget, 'form': form}
    return render(request, 'budgets/edit.html', context)


def budget_delete(request, slug):
    """
    Delete a budget object.
    """
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    if request.POST:
        if request.POST.get('confirmed'):
            budget.delete()
        return HttpResponseRedirect(reverse('budget:budget_budget_list'))
    context = {'budget': budget}
    return render(request, 'budgets/delete.html', context)


def estimate_list(request, slug):
    """
    A list of estimate objects.
    """
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    estimates_list = BudgetEstimate.active.all()
    try:
        paginator = Paginator(estimates_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        estimates = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    context = {
        'budget': budget,
        'estimates': estimates,
        'paginator': paginator,
        'page': page,
    }
    return render(request, 'estimates/list.html', context)


def estimate_add(request, slug):
    """
    Create a new estimate object.
    """
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    if request.POST:
        form = BudgetEstimateForm(request.POST)

        if form.is_valid():
            estimate = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget:budget_estimate_list', kwargs={'slug': budget.slug}))
    else:
        form = BudgetEstimateForm()
    context = {'budget': budget, 'form': form}
    return render(request, 'estimates/add.html', context)


def estimate_edit(request, slug, pk):
    """
    Edit a estimate object.
    """
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    try:
        estimate = budget.estimates.get(pk=pk, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        form = BudgetEstimateForm(request.POST, instance=estimate)

        if form.is_valid():
            category = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget:budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = BudgetEstimateForm(instance=estimate)
    context = {'budget': budget, 'estimate': estimate, 'form': form}
    return render(request, 'estimates/edit.html', context)


def estimate_delete(request, slug, pk):
    """
    Delete a estimate object.
    """
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    try:
        estimate = budget.estimates.get(pk=pk, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        if request.POST.get('confirmed'):
            estimate.delete()
        return HttpResponseRedirect(reverse('budget:budget_estimate_list', kwargs={'slug': budget.slug}))
    context = {'budget': budget, 'estimate': estimate}
    return render(request, 'estimates/delete.html', context)
