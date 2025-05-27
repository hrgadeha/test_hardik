// Copyright (c) 2025, Hardik Gadesha and contributors
// For license information, please see license.txt

frappe.query_reports["Solar Cell Monthly KWH Tariff Report"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": "Customer",
			"fieldtype": "Link",
			"options": "Customer",
			"default": "",
			"reqd": 0
		},
		{
			"fieldname": "year",
			"label": "Year",
			"fieldtype": "Select",
			"options": ["2024","2025","2026","2027","2028","2029","2030"],
			"default": "2025",
			"reqd": 1
		}
	]
};
