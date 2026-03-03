from django.utils.translation import gettext_lazy as _

MODULE_ID = 'tax'
MODULE_NAME = _('Tax Management')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'receipt-outline'
MODULE_DESCRIPTION = _('Tax rates, calculations and reporting')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'finance'

MENU = {
    'label': _('Tax Management'),
    'icon': 'receipt-outline',
    'order': 50,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Tax Rates'), 'icon': 'receipt-outline', 'id': 'rates'},
{'label': _('Reports'), 'icon': 'bar-chart-outline', 'id': 'reports'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'tax.view_taxrate',
'tax.add_taxrate',
'tax.change_taxrate',
'tax.view_taxreport',
'tax.add_taxreport',
'tax.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_taxrate",
        "add_taxreport",
        "change_taxrate",
        "view_taxrate",
        "view_taxreport",
    ],
    "employee": [
        "add_taxrate",
        "view_taxrate",
        "view_taxreport",
    ],
}
