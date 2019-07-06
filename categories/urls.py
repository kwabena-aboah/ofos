from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('', views.category_list, name="budget_category_list"),
    path('add/', views.category_add, name="budget_category_add"),
    path('edit/<slug:slug>/', views.category_edit, name='budget_category_edit'),
    path('delete/<slug:slug>/', views.category_delete, name='budget_category_delete'),
]
