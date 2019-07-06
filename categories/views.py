from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Category
from .forms import CategoryForm


def category_list(request):
    """
    A list of category objects.
    """
    categories_list = Category.active.all()
    try:
        paginator = Paginator(categories_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        categories = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    context = {'categories': categories, 'paginator': paginator, 'page': page,}
    return render(request, 'categories/list.html', context)


def category_add(request):
    """
    Create a new category object.
    """
    if request.POST:
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('categories:budget_category_list'))
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'categories/add.html', context)


def category_edit(request, slug):
    """
    Edit a category object.
    """
    category = get_object_or_404(Category.active.all(), slug=slug)
    if request.POST:
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('categories:budget_category_list'))
    else:
        form = CategoryForm(instance=category)
    context =  {'category': category, 'form': form}
    return render(request, 'categories/edit.html', context)


def category_delete(request, slug):
    """
    Delete a category object.
    """
    category = get_object_or_404(Category.active.all(), slug=slug)
    if request.POST:
        if request.POST.get('confirmed') and request.POST['confirmed'] == 'Yes':
            category.delete()
        return HttpResponseRedirect(reverse('categories:budget_category_list'))
    context = {'category': category}
    return render(request, 'categories/delete.html', context)
