# Tax Management

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `tax` |
| **Version** | `1.0.0` |
| **Icon** | `receipt-outline` |
| **Dependencies** | None |

## Models

### `TaxRate`

TaxRate(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, rate, tax_type, is_default, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=100 |
| `rate` | DecimalField |  |
| `tax_type` | CharField | max_length=30 |
| `is_default` | BooleanField |  |
| `is_active` | BooleanField |  |

### `TaxReport`

TaxReport(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, period_start, period_end, total_collected, total_paid, net_amount, status)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `period_start` | DateField |  |
| `period_end` | DateField |  |
| `total_collected` | DecimalField |  |
| `total_paid` | DecimalField |  |
| `net_amount` | DecimalField |  |
| `status` | CharField | max_length=20 |

## URL Endpoints

Base path: `/m/tax/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `rates/` | `rates` | GET |
| `reports/` | `reports` | GET |
| `tax_rates/` | `tax_rates_list` | GET |
| `tax_rates/add/` | `tax_rate_add` | GET/POST |
| `tax_rates/<uuid:pk>/edit/` | `tax_rate_edit` | GET |
| `tax_rates/<uuid:pk>/delete/` | `tax_rate_delete` | GET/POST |
| `tax_rates/<uuid:pk>/toggle/` | `tax_rate_toggle_status` | GET |
| `tax_rates/bulk/` | `tax_rates_bulk_action` | GET/POST |
| `tax_reports/` | `tax_reports_list` | GET |
| `tax_reports/add/` | `tax_report_add` | GET/POST |
| `tax_reports/<uuid:pk>/edit/` | `tax_report_edit` | GET |
| `tax_reports/<uuid:pk>/delete/` | `tax_report_delete` | GET/POST |
| `tax_reports/bulk/` | `tax_reports_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `tax.view_taxrate` | View Taxrate |
| `tax.add_taxrate` | Add Taxrate |
| `tax.change_taxrate` | Change Taxrate |
| `tax.view_taxreport` | View Taxreport |
| `tax.add_taxreport` | Add Taxreport |
| `tax.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_taxrate`, `add_taxreport`, `change_taxrate`, `view_taxrate`, `view_taxreport`
- **employee**: `add_taxrate`, `view_taxrate`, `view_taxreport`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Tax Rates | `receipt-outline` | `rates` | No |
| Reports | `bar-chart-outline` | `reports` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_tax_rates`

List tax rates.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_active` | boolean | No |  |
| `tax_type` | string | No |  |

### `create_tax_rate`

Create a tax rate.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `rate` | string | Yes |  |
| `tax_type` | string | No |  |
| `is_default` | boolean | No |  |

### `list_tax_reports`

List tax reports.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No |  |
| `limit` | integer | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  tax/
    css/
    js/
templates/
  tax/
    pages/
      dashboard.html
      index.html
      rates.html
      reports.html
      settings.html
      tax_rate_add.html
      tax_rate_edit.html
      tax_rates.html
      tax_report_add.html
      tax_report_edit.html
      tax_reports.html
    partials/
      dashboard_content.html
      panel_tax_rate_add.html
      panel_tax_rate_edit.html
      panel_tax_report_add.html
      panel_tax_report_edit.html
      rates_content.html
      reports_content.html
      settings_content.html
      tax_rate_add_content.html
      tax_rate_edit_content.html
      tax_rates_content.html
      tax_rates_list.html
      tax_report_add_content.html
      tax_report_edit_content.html
      tax_reports_content.html
      tax_reports_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
