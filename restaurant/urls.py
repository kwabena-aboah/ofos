from django.urls import path
from . import views
from .views import ReportView, general_report, ChartData

app_name = 'restaurant'
urlpatterns = [
	path('', views.index, name='index'),
	path('order/<int:order_id>/', views.show, name='show'),
	path('new_order/', views.new_order, name='new_order'),
	path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
	path('delete_order/<int:order_id>/',views.delete_order, name='delete_order'),
	path('foods/', views.foods, name='foods'),
	path('new_food/', views.new_food, name='new_food'),
	path('delete_food/<int:food_id>/', views.delete_food, name='delete_food'),
	path('reports/', ReportView.as_view(), name='reports'),
	path('api/data/', general_report, name='api-data'),
	path('api/chart/data/', ChartData.as_view()),
]
