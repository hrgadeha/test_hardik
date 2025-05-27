# 🌞 Solar Cell ROI Calculation System

This system is developed to calculate the **Return on Investment (ROI)** for clients switching to solar energy by analyzing average power consumption and tariffs over time.

## ✅ Objectives

- Track **KW (15-minute)** and **KWH (hourly)** power consumption for customers.
- Calculate **monthly average consumption and tariffs** for high and low tariff periods.
- Provide reports to support **financial analysis and decision making** for solar energy use.

## 📁 Modules and DocTypes

### 1. Customer
- Maintains customer records.
- Linked with all energy consumption entries.

### 2. Solar Cell KW Reading Entry
- Captures 15-minute **KW readings**.
- Fields include: customer, reading datetime, KW value.
- Tariff type, tariff, month and year will be auto set
- Entries are **submittable** and auto-serialized per customer.

### 3. Solar Cell KWH Reading Entry
- Captures hourly **KWH readings**.
- Similar structure to KW entries but focused on energy over time.

### 4. Solar Cell Tariff Configuration
- Manages:
  - Time ranges for **low** (11:00 PM – 5:59 AM) and **high** (6:00 AM – 10:59 PM) tariff periods.
  - Tariff rates for each period.
  - Configuration is used during calculations.

## 📊 Reports

### 🔹 KW Tariff Report
- Calculates and displays:
  - Average low/high **KW consumption** per customer per month.
  - Average **low/high tariffs** using formula:
    - `Low Tariff = 0.1 * Avg KWH in low period`
    - `High Tariff = 0.3 * Avg KWH in high period`

### 🔹 KWH Tariff Report
- Similar to the KW report but focused on **hourly KWH readings**.

## 🔐 User Permissions

- **Sales Team**:
  - Can **create and submit** KW and KWH entries.
- **Accounting Team**:
  - Has **read-only** access to consumption entries and reports.

## 📥 Data Source

- Supports importing data from Excel files.
- All Excel fields are mapped and included in entry forms.
EOF