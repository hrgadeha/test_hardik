# Copyright (c) 2025, Hardik Gadesha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from test_hardik.test_data_generation import is_low_tariff
from datetime import datetime, time

class SolarCellKWHReadingEntry(Document):
	def validate(self):
		# Convert reading_date to a date object if it's a string
		if isinstance(self.reading_date, str):
			reading_date = datetime.strptime(self.reading_date, "%Y-%m-%d").date()
		else:
			reading_date = self.reading_date

		# Convert reading_time to a time object
		if isinstance(self.reading_time, str):
			# Try parsing with seconds (HH:MM:SS), fallback to without seconds (HH:MM)
			try:
				reading_time = datetime.strptime(self.reading_time, "%H:%M:%S").time()
			except ValueError:
				reading_time = datetime.strptime(self.reading_time, "%H:%M").time()
		else:
			reading_time = self.reading_time

		# Set month and year for tariff calculation
		self.tariff_month = reading_date.strftime("%B")
		self.tariff_year = reading_date.year

		# Fetch tariff configurations valid on the reading date
		tariff_configurations = frappe.get_all(
			"Solar Cell Tariff Configuration",
			fields="*",
			filters={
				"valid_from": ["<=", self.reading_date],
				"valid_to": [">=", self.reading_date],
				"enable": True
			}
		)

		# Exit if no matching tariff configuration is found
		if not tariff_configurations:
			return

		# Get applicable tariff from the list based on reading date
		applicable_tariff = self.get_applicable_tariff(tariff_configurations, reading_date)
		if not applicable_tariff:
			return

		# Determine tariff type based on reading time and assign rate
		if is_low_tariff(applicable_tariff, reading_time):
			self.tariff_type = "Low Tariff"
			self.tariff = applicable_tariff.low_tariff_rate
		else:
			self.tariff_type = "High Tariff"
			self.tariff = applicable_tariff.high_tariff_rate


	def get_applicable_tariff(self, tariff_configurations, target_date):
		# Ensure target_date is a datetime.date object
		if isinstance(target_date, str):
			target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
		elif isinstance(target_date, datetime):
			target_date = target_date.date()

		# Loop through all tariff configurations
		for tariff in tariff_configurations:
			# Parse valid_from if it's a string
			start_date = tariff["valid_from"]
			if isinstance(start_date, str):
				start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

			# Parse valid_to if it's a string
			end_date = tariff["valid_to"]
			if isinstance(end_date, str):
				end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

			# Return the configuration if target_date falls in the range
			if start_date <= target_date <= end_date:
				return tariff

		# Return None if no configuration matches the target_date
		return None