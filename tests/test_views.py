"""Tests for tax views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('tax:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('tax:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('tax:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestTaxRateViews:
    """TaxRate view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('tax:tax_rates_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('tax:tax_rates_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('tax:tax_rates_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('tax:tax_rates_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('tax:tax_rates_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('tax:tax_rates_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('tax:tax_rate_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('tax:tax_rate_add')
        data = {
            'name': 'New Name',
            'rate': '100.00',
            'tax_type': 'New Tax Type',
            'is_default': 'on',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, tax_rate):
        """Test edit form loads."""
        url = reverse('tax:tax_rate_edit', args=[tax_rate.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, tax_rate):
        """Test editing via POST."""
        url = reverse('tax:tax_rate_edit', args=[tax_rate.pk])
        data = {
            'name': 'Updated Name',
            'rate': '100.00',
            'tax_type': 'Updated Tax Type',
            'is_default': '',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, tax_rate):
        """Test soft delete via POST."""
        url = reverse('tax:tax_rate_delete', args=[tax_rate.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        tax_rate.refresh_from_db()
        assert tax_rate.is_deleted is True

    def test_toggle_status(self, auth_client, tax_rate):
        """Test toggle active status."""
        url = reverse('tax:tax_rate_toggle_status', args=[tax_rate.pk])
        original = tax_rate.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        tax_rate.refresh_from_db()
        assert tax_rate.is_active != original

    def test_bulk_delete(self, auth_client, tax_rate):
        """Test bulk delete."""
        url = reverse('tax:tax_rates_bulk_action')
        response = auth_client.post(url, {'ids': str(tax_rate.pk), 'action': 'delete'})
        assert response.status_code == 200
        tax_rate.refresh_from_db()
        assert tax_rate.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('tax:tax_rates_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestTaxReportViews:
    """TaxReport view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('tax:tax_reports_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('tax:tax_reports_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('tax:tax_reports_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('tax:tax_reports_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('tax:tax_reports_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('tax:tax_reports_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('tax:tax_report_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('tax:tax_report_add')
        data = {
            'name': 'New Name',
            'period_start': '2025-01-15',
            'period_end': '2025-01-15',
            'total_collected': '100.00',
            'total_paid': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, tax_report):
        """Test edit form loads."""
        url = reverse('tax:tax_report_edit', args=[tax_report.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, tax_report):
        """Test editing via POST."""
        url = reverse('tax:tax_report_edit', args=[tax_report.pk])
        data = {
            'name': 'Updated Name',
            'period_start': '2025-01-15',
            'period_end': '2025-01-15',
            'total_collected': '100.00',
            'total_paid': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, tax_report):
        """Test soft delete via POST."""
        url = reverse('tax:tax_report_delete', args=[tax_report.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        tax_report.refresh_from_db()
        assert tax_report.is_deleted is True

    def test_bulk_delete(self, auth_client, tax_report):
        """Test bulk delete."""
        url = reverse('tax:tax_reports_bulk_action')
        response = auth_client.post(url, {'ids': str(tax_report.pk), 'action': 'delete'})
        assert response.status_code == 200
        tax_report.refresh_from_db()
        assert tax_report.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('tax:tax_reports_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('tax:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('tax:settings')
        response = client.get(url)
        assert response.status_code == 302

