# Copyright (c) 2025, Hardik Gadesha and contributors
# For license information, please see license.txt

import frappe
from collections import defaultdict

def execute(filters=None):
	# Initialize filters if None provided
	if not filters:
		filters = {}

	# Extract the year filter and optional customer filter from input
	selected_year = int(filters.get("year"))
	selected_customer = filters.get("customer")

	# Define the order of months starting from April (for financial year)
	financial_year_months = [
		"April", "May", "June", "July", "August", "September",
		"October", "November", "December", "January", "February", "March"
	]

	# Define columns for the report output
	columns = [
		"Customer:Link/Customer:200",    # Link to Customer
		"Customer Name:Data:200"          # Customer name as text
	]

	# For each month, add columns for Avg Low KWH, Low Tariff, Avg High KWH, High Tariff
	for month in financial_year_months:
		columns.extend([
			f"{month} Avg Low KWH:Float",
			f"{month} Avg Low Tariff:Currency",
			f"{month} Avg High KWH:Float",
			f"{month} Avg High Tariff:Currency"
		])

	# Build filters to fetch relevant readings
	reading_filters = {
		"docstatus": 1,  # Only submitted documents
		"tariff_year": ["in", [selected_year, selected_year + 1]],  # Current and next year readings
	}
	if selected_customer:
		reading_filters["customer"] = selected_customer

	# Fetch readings from the DocType "Solar Cell KWH Reading Entry"
	readings = frappe.get_all(
		"Solar Cell KWH Reading Entry",
		filters=reading_filters,
		fields=[
			"customer",
			"customer_name",
			"tariff_month",
			"tariff_year",
			"kwh_value",
			"tariff_type",
			"tariff"  # tariff rate per entry
		]
	)

	# Data structure to accumulate sums and counts per customer and month
	# Now also accumulate total tariff amounts based on kwh_value * tariff rate
	summary_data = defaultdict(lambda: defaultdict(lambda: {
		"low_kwh_sum": 0, "low_kwh_count": 0, "low_tariff_sum": 0,
		"high_kwh_sum": 0, "high_kwh_count": 0, "high_tariff_sum": 0
	}))

	# Store customer names for display
	customer_name_map = {}

	# Process each reading entry
	for reading in readings:
		customer_id = reading.customer
		month = reading.tariff_month
		kwh_value = reading.kwh_value or 0
		tariff_category = (reading.tariff_type or "").strip()
		tariff_rate = reading.tariff or 0  # read tariff rate per entry

		# Store customer name (assuming consistent per customer)
		customer_name_map[customer_id] = reading.customer_name

		# Accumulate KWH and tariff amounts based on tariff type
		if tariff_category == "Low Tariff":
			summary_data[customer_id][month]["low_kwh_sum"] += kwh_value
			summary_data[customer_id][month]["low_kwh_count"] += 1
			summary_data[customer_id][month]["low_tariff_sum"] += kwh_value * tariff_rate
		elif tariff_category == "High Tariff":
			summary_data[customer_id][month]["high_kwh_sum"] += kwh_value
			summary_data[customer_id][month]["high_kwh_count"] += 1
			summary_data[customer_id][month]["high_tariff_sum"] += kwh_value * tariff_rate

	# Prepare final data rows for the report
	report_data = []
	for customer_id, monthly_data in summary_data.items():
		row = [customer_id, customer_name_map.get(customer_id, "")]

		# For each month in financial year, calculate averages and tariffs
		for month in financial_year_months:
			month_data = monthly_data.get(month, {})

			# Calculate average Low Tariff KWH and tariff amount (use accumulated sums)
			low_avg_kwh = round(
				month_data.get("low_kwh_sum", 0) / month_data.get("low_kwh_count", 1), 2
			) if month_data.get("low_kwh_count") else 0
			low_avg_tariff = round(
				month_data.get("low_tariff_sum", 0) / month_data.get("low_kwh_count", 1), 2
			) if month_data.get("low_kwh_count") else 0

			# Calculate average High Tariff KWH and tariff amount
			high_avg_kwh = round(
				month_data.get("high_kwh_sum", 0) / month_data.get("high_kwh_count", 1), 2
			) if month_data.get("high_kwh_count") else 0
			high_avg_tariff = round(
				month_data.get("high_tariff_sum", 0) / month_data.get("high_kwh_count", 1), 2
			) if month_data.get("high_kwh_count") else 0

			# Append calculated values to the row
			row.extend([low_avg_kwh, low_avg_tariff, high_avg_kwh, high_avg_tariff])

		report_data.append(row)

	return columns, report_data