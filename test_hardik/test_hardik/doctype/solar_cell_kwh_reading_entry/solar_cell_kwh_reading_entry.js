// Copyright (c) 2025, Hardik Gadesha and contributors
// For license information, please see license.txt

frappe.ui.form.on("Solar Cell KWH Reading Entry", {
	from_time(frm) {
        validateTimeRange(frm);
	},
    to_time(frm) {
        validateTimeRange(frm);
	},
});

function validateKWDateTime(inputDateTime) {
    const date = new Date(inputDateTime);
    const minutes = date.getMinutes();

    if (![0, 15, 30, 45].includes(minutes)) {
        alert("KW datetime must be at exact 15-minute intervals (e.g., 12:00, 12:15, 12:30, 12:45).");
        return false;
    }
    return true;
}