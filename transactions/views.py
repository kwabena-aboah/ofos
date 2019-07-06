from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Transaction
from .forms import TransactionForm


def transaction_list(request):
    """
    A list of transaction objects.
    """
    transaction_list = Transaction.active.order_by('-date', '-created')
    try:
        paginator = Paginator(transaction_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        transactions = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    context = {'transactions': transactions, 'paginator': paginator, 'page': page}
    return render(request, 'transactions/list.html', context)


def transaction_add(request):
    """
    Create a new transaction object.
    """
    if request.POST:
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save()
            return HttpResponseRedirect(reverse('transactions:budget_transaction_list'))
    else:
        form = TransactionForm()
    context = {'form': form}
    return render(request, 'transactions/add.html', context)


def transaction_edit(request, pk):
    """
    Edit a transaction object.
    """
    transaction = get_object_or_404(Transaction.active.all(), pk=pk)
    if request.POST:
        form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('transactions:budget_transaction_list'))
    else:
        form = TransactionForm(instance=transaction)
    context = {'transaction': transaction, 'form': form}
    return render(request, 'transactions/edit.html', context)


def transaction_delete(request, pk):
    """
    Delete a transaction object.
    """
    transaction = get_object_or_404(Transaction.active.all(), pk=pk)
    if request.POST:
        if request.POST.get('confirmed'):
            transaction.delete()
        return HttpResponseRedirect(reverse('transactions:budget_transaction_list'))
    context = {'transaction': transaction}
    return render(request, 'transactions/delete.html', context)
