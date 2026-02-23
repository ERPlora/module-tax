"""
Tax Management Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('tax', 'dashboard')
@htmx_view('tax/pages/dashboard.html', 'tax/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('tax', 'rates')
@htmx_view('tax/pages/rates.html', 'tax/partials/rates_content.html')
def rates(request):
    """Tax Rates view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('tax', 'reports')
@htmx_view('tax/pages/reports.html', 'tax/partials/reports_content.html')
def reports(request):
    """Reports view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('tax', 'settings')
@htmx_view('tax/pages/settings.html', 'tax/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

