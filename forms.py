from django import forms
from django.utils.translation import gettext_lazy as _

from .models import TaxRate, TaxReport

class TaxRateForm(forms.ModelForm):
    class Meta:
        model = TaxRate
        fields = ['name', 'rate', 'tax_type', 'is_default', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'rate': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'tax_type': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class TaxReportForm(forms.ModelForm):
    class Meta:
        model = TaxReport
        fields = ['name', 'period_start', 'period_end', 'total_collected', 'total_paid', 'net_amount', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'period_start': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'period_end': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'total_collected': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'total_paid': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'net_amount': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }

