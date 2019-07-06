from django.urls import path
from . import views

app_name = 'transactions'
urlpatterns = [
    path('', views.transaction_list, name='budget_transaction_list'),
    path('add/', views.transaction_add, name='budget_transaction_add'),
    path('edit/<int:pk>/', views.transaction_edit, name='budget_transaction_edit'),
    path('delete/<int:pk>/', views.transaction_delete, name='budget_transaction_delete'),
]
