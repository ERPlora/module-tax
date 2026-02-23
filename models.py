from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class TaxRate(HubBaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Rate'))
    tax_type = models.CharField(max_length=30, default='vat', verbose_name=_('Tax Type'))
    is_default = models.BooleanField(default=False, verbose_name=_('Is Default'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'tax_taxrate'

    def __str__(self):
        return self.name


class TaxReport(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    period_start = models.DateField(verbose_name=_('Period Start'))
    period_end = models.DateField(verbose_name=_('Period End'))
    total_collected = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Total Collected'))
    total_paid = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Total Paid'))
    net_amount = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Net Amount'))
    status = models.CharField(max_length=20, default='draft', verbose_name=_('Status'))

    class Meta(HubBaseModel.Meta):
        db_table = 'tax_taxreport'

    def __str__(self):
        return self.name

