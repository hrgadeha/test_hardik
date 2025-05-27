## Test Hardik

The Solar ROI Calculator is a Frappe-based application designed to help solar energy companies assess the return on investment (ROI) for clients considering a switch to solar power. It provides accurate consumption-based calculations using energy usage data (in KW and KWH), supports time-of-use tariff modeling, and generates monthly savings insights.

#### License

mit

## Features

- Processes power consumption data recorded hourly (KWH) and every 15 minutes (KW) for each customer.
- Calculates average KW and KWH values for all records.
- Computes monthly average low and high tariffs based on consumption during defined tariff periods in configuration:
  - **Low tariff period:** 11:00 PM – 5:59 AM (eg.)
  - **High tariff period:** 6:00 AM – 10:59 PM (eg.)
- Applies tariff formulas for each month as per configuration:
  - Low tariff = 0.1 × Average KWH during low tariff period (eg.)
  - High tariff = 0.3 × Average KWH during high tariff period (eg.)
- Supports entry creation for customers at any time, allowing flexible data input.

## Installation

1. Ensure you have [Frappe Framework](https://frappeframework.com/docs/user/en/installation) installed.
2. Clone this repository into your bench's apps directory:

```bash
    cd frappe-bench/apps
    bench get-app --branch main https://github.com/hrgadeha/test_hardik
```

3. Install the app on your site:

```bash
    cd frappe-bench
    bench --site your-site-name install-app test_hardik
```

4. Restart the bench:

```bash
    bench restart
```

## Usage

- Enter hourly and 15-minute power consumption data for customers.
- Use provided reports or scripts to view average consumption and tariff calculations.
- Analyze ROI based on computed tariffs and consumption averages.

## Development

- Setup a development site and install the app for testing.
- Customize calculations or add new features as needed.

## Contributing

- Contributions, issues, and feature requests are welcome.
- Please follow Frappe best practices for code style and structure.

## Support

- For support or queries, contact hardikgadesha@gmail.com or raise issues on the repository.

*This README provides an overview of the solar power consumption and tariff calculation system within the `test_hardik` app.*