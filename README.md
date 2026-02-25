# Tax Management Module

Tax rates, calculations and reporting.

## Features

- Define tax rates with name, percentage, type (e.g., VAT), and default/active flags
- Generate tax reports for specific periods with collected, paid, and net amounts
- Track report status (draft, finalized, etc.)
- Set a default tax rate for automatic application
- Dashboard with tax overview and period summaries

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Tax Management > Settings**

## Usage

Access via: **Menu > Tax Management**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/tax/dashboard/` | Tax overview and period summaries |
| Tax Rates | `/m/tax/rates/` | Create and manage tax rates |
| Reports | `/m/tax/reports/` | Generate and view tax reports by period |
| Settings | `/m/tax/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `TaxRate` | Tax rate definition with name, percentage rate, tax type, default flag, and active status |
| `TaxReport` | Tax report for a period with name, start/end dates, total collected, total paid, net amount, and status |

## Permissions

| Permission | Description |
|------------|-------------|
| `tax.view_taxrate` | View tax rates |
| `tax.add_taxrate` | Create new tax rates |
| `tax.change_taxrate` | Edit existing tax rates |
| `tax.view_taxreport` | View tax reports |
| `tax.add_taxreport` | Generate new tax reports |
| `tax.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
