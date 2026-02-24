"""Tests for tax models."""
import pytest
from django.utils import timezone

from tax.models import TaxRate, TaxReport


@pytest.mark.django_db
class TestTaxRate:
    """TaxRate model tests."""

    def test_create(self, tax_rate):
        """Test TaxRate creation."""
        assert tax_rate.pk is not None
        assert tax_rate.is_deleted is False

    def test_str(self, tax_rate):
        """Test string representation."""
        assert str(tax_rate) is not None
        assert len(str(tax_rate)) > 0

    def test_soft_delete(self, tax_rate):
        """Test soft delete."""
        pk = tax_rate.pk
        tax_rate.is_deleted = True
        tax_rate.deleted_at = timezone.now()
        tax_rate.save()
        assert not TaxRate.objects.filter(pk=pk).exists()
        assert TaxRate.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, tax_rate):
        """Test default queryset excludes deleted."""
        tax_rate.is_deleted = True
        tax_rate.deleted_at = timezone.now()
        tax_rate.save()
        assert TaxRate.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, tax_rate):
        """Test toggling is_active."""
        original = tax_rate.is_active
        tax_rate.is_active = not original
        tax_rate.save()
        tax_rate.refresh_from_db()
        assert tax_rate.is_active != original


@pytest.mark.django_db
class TestTaxReport:
    """TaxReport model tests."""

    def test_create(self, tax_report):
        """Test TaxReport creation."""
        assert tax_report.pk is not None
        assert tax_report.is_deleted is False

    def test_str(self, tax_report):
        """Test string representation."""
        assert str(tax_report) is not None
        assert len(str(tax_report)) > 0

    def test_soft_delete(self, tax_report):
        """Test soft delete."""
        pk = tax_report.pk
        tax_report.is_deleted = True
        tax_report.deleted_at = timezone.now()
        tax_report.save()
        assert not TaxReport.objects.filter(pk=pk).exists()
        assert TaxReport.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, tax_report):
        """Test default queryset excludes deleted."""
        tax_report.is_deleted = True
        tax_report.deleted_at = timezone.now()
        tax_report.save()
        assert TaxReport.objects.filter(hub_id=hub_id).count() == 0


