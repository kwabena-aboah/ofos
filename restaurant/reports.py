from report_tools.reports import Report
from report_tools.chart_data import ChartData
from report_tools.renderers.googlecharts import GoogleChartsRenderer
from report_tools.charts import *
from . models import Order

class MyReport(Report):
	renderer = GoogleChartsRenderer
	pie_chart = charts.PieChart(
		title="Order Reports",
		width=400,
		height=300
	)
	def get_data_for_pie_chart(self):
		orders = Order.objects.all()

		for order in orders:
			amount = float((order.food_id.price * order.quantity) + order.food_id.vat)
			data = ChartData()
			data.add_column(order.order_date)
			# data.add_column("Population")
			data.add_row(["2019", amount])
			data.add_row(["2020", amount])	
			data.add_row(["2021", amount])
		return data
