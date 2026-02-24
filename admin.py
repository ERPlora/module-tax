from django.contrib import admin

from .models import TaxRate, TaxReport

@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate', 'tax_type', 'is_default', 'is_active', 'created_at']
    search_fields = ['name', 'tax_type']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TaxReport)
class TaxReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'period_start', 'period_end', 'total_collected', 'total_paid', 'created_at']
    search_fields = ['name', 'status']
    readonly_fields = ['created_at', 'updated_at']

