from datetime import datetime, timedelta, time
import random
import frappe

def generate_hourly_kwh_readings():
	try:
		# Define start and end datetime for the hourly generation
		start_datetime = datetime(2025, 4, 1, 0, 0)
		end_datetime = datetime(2025, 5, 31, 23, 0)  # Include the last hour of May 31

		# Fetch all customers
		customer_list = get_active_customers()

		current_datetime = start_datetime
		tariffs_for_the_day = None
		last_checked_date = None

		# Loop through each hour in the given date range
		while current_datetime <= end_datetime:
			current_date = current_datetime.date()

			# Refresh tariff configurations only when the date changes
			if last_checked_date != current_date:
				last_checked_date = current_date

				# Fetch tariff configurations that are valid and enabled on the current day
				tariffs_for_the_day = frappe.get_all(
					"Solar Cell Tariff Configuration",
					fields="*",
					filters={
						"valid_from": ["<=", current_date],
						"valid_to": [">=", current_date],
						"enable": True
					}
				)

			# Iterate through each customer and insert an hourly KWH reading
			for customer in customer_list:
				applicable_tariff = get_applicable_tariff(tariffs_for_the_day, current_datetime)
				if not applicable_tariff:
					continue  # Skip if no applicable tariff

				# Determine tariff type and rate based on the current time
				if is_low_tariff(applicable_tariff, current_datetime.time()):
					tariff_type = "Low Tariff"
					tariff_rate = applicable_tariff.low_tariff_rate
				else:
					tariff_type = "High Tariff"
					tariff_rate = applicable_tariff.high_tariff_rate

				# Simulate a random KWH value between 1.5 and 8.5
				kwh_value = round(random.uniform(1.5, 8.5), 2)

				# Prepare and insert the reading entry
				frappe.get_doc({
					"doctype": "Solar Cell KWH Reading Entry",
					"customer": customer.name,
					"customer_name": customer.customer_name,
					"reading_date": current_datetime.date(),
					"reading_time": current_datetime.time(),
					"kwh_value": kwh_value,
					"tariff_type": tariff_type,
					"tariff": tariff_rate,
					"tariff_year": current_datetime.year,
					"tariff_month": current_datetime.strftime("%B")
				}).insert(ignore_permissions=True)

			# Move to the next hour
			current_datetime += timedelta(hours=1)

		# Commit all inserted records
		frappe.db.commit()

	except Exception:
		frappe.log_error(frappe.get_traceback(), "Error in generate_hourly_kwh_readings")


def generate_kw_readings_every_15_min():
	try:
		# Define the date range from April 1 to May 31, 2025, inclusive
		start_datetime = datetime(2025, 4, 1, 0, 0)
		end_datetime = datetime(2025, 5, 31, 23, 45)  # Include last 15-minute interval

		# Fetch all customer records
		customer_list = get_active_customers()

		current_datetime = start_datetime
		tariffs_for_the_day = None
		last_checked_date = None

		# Iterate in 15-minute intervals
		while current_datetime <= end_datetime:
			current_date = current_datetime.date()

			# Refresh tariff configuration if date has changed
			if last_checked_date != current_date:
				last_checked_date = current_date

				# Get enabled tariffs applicable on the current date
				tariffs_for_the_day = frappe.get_all(
					"Solar Cell Tariff Configuration",
					fields="*",
					filters={
						"valid_from": ["<=", current_date],
						"valid_to": [">=", current_date],
						"enable": True
					}
				)

			# Loop through each customer to generate a reading
			for customer in customer_list:
				applicable_tariff = get_applicable_tariff(tariffs_for_the_day, current_datetime)
				if not applicable_tariff:
					continue  # Skip if no tariff applies

				# Determine the tariff type and rate based on time
				if is_low_tariff(applicable_tariff, current_datetime.time()):
					tariff_type = "Low Tariff"
					tariff_rate = applicable_tariff.low_tariff_rate
				else:
					tariff_type = "High Tariff"
					tariff_rate = applicable_tariff.high_tariff_rate

				# Simulate a random KW value (you can replace with real logic)
				kw_value = round(random.uniform(1.5, 8.5), 2)

				# Prepare and insert the KW reading entry
				frappe.get_doc({
					"doctype": "Solar Cell KW Reading Entry",
					"customer": customer.name,
					"customer_name": customer.customer_name,
					"reading_date": current_datetime.date(),
					"reading_time": current_datetime.time(),
					"kw_value": kw_value,
					"tariff_type": tariff_type,
					"tariff": tariff_rate,
					"tariff_year": current_datetime.year,
					"tariff_month": current_datetime.strftime("%B")
				}).insert(ignore_permissions=True)

			# Move to the next 15-minute interval
			current_datetime += timedelta(minutes=15)

		# Commit all the inserts to the database
		frappe.db.commit()

	except Exception:
		frappe.log_error(frappe.get_traceback(), "Error in generate_kw_readings_every_15_min")


def get_applicable_tariff(tariff_list, datetime_obj):
	"""
	Returns the first tariff from the list that is valid for the given datetime.

	Args:
		tariff_list (list): List of tariff dicts or objects.
		datetime_obj (datetime): Current datetime.

	Returns:
		tariff (dict/object) or None: Applicable tariff or None if not found.
	"""
	for tariff in tariff_list:
		if tariff.valid_from <= datetime_obj.date() <= tariff.valid_to:
			return tariff
	return None

def is_low_tariff(tariff, current_time):
	"""
	Checks if the given time falls within the low tariff time range.

	Args:
		tariff (object): Tariff object with `low_tariff_start` and `low_tariff_end`.
		current_time (datetime.time): The time to check.

	Returns:
		bool: True if current_time is within low tariff range, else False.
	"""
	def convert_to_time(value):
		"""Converts a timedelta or time to a time object."""
		if isinstance(value, time):
			return value
		if isinstance(value, timedelta):
			total_seconds = int(value.total_seconds())
			hours = (total_seconds // 3600) % 24
			minutes = (total_seconds % 3600) // 60
			seconds = total_seconds % 60
			return time(hour=hours, minute=minutes, second=seconds)
		return None

	low_start_time = convert_to_time(tariff.low_tariff_start)
	low_end_time = convert_to_time(tariff.low_tariff_end)

	# Return False if tariff times are invalid or missing
	if not low_start_time or not low_end_time:
		return False

	# Handle normal time range (e.g., 02:00 to 06:00)
	if low_start_time < low_end_time:
		return low_start_time <= current_time < low_end_time
	# Handle overnight time range (e.g., 22:00 to 06:00)
	else:
		return current_time >= low_start_time or current_time < low_end_time

def get_active_customers():
	customer_list = frappe.get_all(
		"Customer",
		fields=["name", "customer_name"],
		filters={"enable": 1}
	)

	return customer_list