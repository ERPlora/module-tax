from django.contrib import admin

from .models import TaxRate, TaxReport

@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate', 'tax_type', 'is_default', 'is_active']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(TaxReport)
class TaxReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'period_start', 'period_end', 'total_collected', 'total_paid']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

