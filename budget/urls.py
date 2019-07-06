from django.urls import path
from . import views

app_name = 'budget'
urlpatterns = [
    path('dashboard/', views.dashboard, name='budget_dashboard'),
    path('setup/', views.setup, name='budget_setup'),
    # Summaries
    path('summary/', views.summary_list, name='budget_summary_list'),
    path('summary/<int:year>/', views.summary_year, name='budget_summary_year'),
    path('summary/<int:year>/<int:month>/', views.summary_month, name='budget_summary_month'),
    # Budget
    path('budget/', views.budget_list, name='budget_budget_list'),
    path('budget/add/', views.budget_add, name='budget_budget_add'),
    path('budget/edit/<slug:slug>/', views.budget_edit, name='budget_budget_edit'),
    path('budget/delete/<slug:slug>/', views.budget_delete, name='budget_budget_delete'),
    # BudgetEstimates
    path('budget/<slug:slug>/estimate/', views.estimate_list, name='budget_estimate_list'),
    path('budget/<slug:slug>/estimate/add/', views.estimate_add, name='budget_estimate_add'),
    path('budget/<slug:slug>/estimate/edit/<int:pk>/', views.estimate_edit, name='budget_estimate_edit'),
    path('budget/<slug:slug>/estimate/delete/<int:pk>/', views.estimate_delete, name='budget_estimate_delete'),
]
