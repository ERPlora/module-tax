"""
Tax Management Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import TaxRate, TaxReport

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('tax', 'dashboard')
@htmx_view('tax/pages/index.html', 'tax/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_tax_rates': TaxRate.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_tax_reports': TaxReport.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# TaxRate
# ======================================================================

TAX_RATE_SORT_FIELDS = {
    'name': 'name',
    'is_default': 'is_default',
    'is_active': 'is_active',
    'rate': 'rate',
    'tax_type': 'tax_type',
    'created_at': 'created_at',
}

def _build_tax_rates_context(hub_id, per_page=10):
    qs = TaxRate.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'tax_rates': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_tax_rates_list(request, hub_id, per_page=10):
    ctx = _build_tax_rates_context(hub_id, per_page)
    return django_render(request, 'tax/partials/tax_rates_list.html', ctx)

@login_required
@with_module_nav('tax', 'rates')
@htmx_view('tax/pages/tax_rates.html', 'tax/partials/tax_rates_content.html')
def tax_rates_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = TaxRate.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(tax_type__icontains=search_query))

    order_by = TAX_RATE_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_default', 'is_active', 'rate', 'tax_type']
        headers = ['Name', 'Is Default', 'Is Active', 'Rate', 'Tax Type']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='tax_rates.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='tax_rates.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'tax/partials/tax_rates_list.html', {
            'tax_rates': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'tax_rates': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def tax_rate_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        rate = request.POST.get('rate', '0') or '0'
        tax_type = request.POST.get('tax_type', '').strip()
        is_default = request.POST.get('is_default') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        obj = TaxRate(hub_id=hub_id)
        obj.name = name
        obj.rate = rate
        obj.tax_type = tax_type
        obj.is_default = is_default
        obj.is_active = is_active
        obj.save()
        return _render_tax_rates_list(request, hub_id)
    return django_render(request, 'tax/partials/panel_tax_rate_add.html', {})

@login_required
def tax_rate_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TaxRate, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.rate = request.POST.get('rate', '0') or '0'
        obj.tax_type = request.POST.get('tax_type', '').strip()
        obj.is_default = request.POST.get('is_default') == 'on'
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_tax_rates_list(request, hub_id)
    return django_render(request, 'tax/partials/panel_tax_rate_edit.html', {'obj': obj})

@login_required
@require_POST
def tax_rate_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TaxRate, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_tax_rates_list(request, hub_id)

@login_required
@require_POST
def tax_rate_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TaxRate, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_tax_rates_list(request, hub_id)

@login_required
@require_POST
def tax_rates_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = TaxRate.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_tax_rates_list(request, hub_id)


# ======================================================================
# TaxReport
# ======================================================================

TAX_REPORT_SORT_FIELDS = {
    'name': 'name',
    'status': 'status',
    'net_amount': 'net_amount',
    'total_paid': 'total_paid',
    'total_collected': 'total_collected',
    'period_start': 'period_start',
    'created_at': 'created_at',
}

def _build_tax_reports_context(hub_id, per_page=10):
    qs = TaxReport.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'tax_reports': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_tax_reports_list(request, hub_id, per_page=10):
    ctx = _build_tax_reports_context(hub_id, per_page)
    return django_render(request, 'tax/partials/tax_reports_list.html', ctx)

@login_required
@with_module_nav('tax', 'rates')
@htmx_view('tax/pages/tax_reports.html', 'tax/partials/tax_reports_content.html')
def tax_reports_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = TaxReport.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(status__icontains=search_query))

    order_by = TAX_REPORT_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'status', 'net_amount', 'total_paid', 'total_collected', 'period_start']
        headers = ['Name', 'Status', 'Net Amount', 'Total Paid', 'Total Collected', 'Period Start']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='tax_reports.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='tax_reports.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'tax/partials/tax_reports_list.html', {
            'tax_reports': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'tax_reports': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def tax_report_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        period_start = request.POST.get('period_start') or None
        period_end = request.POST.get('period_end') or None
        total_collected = request.POST.get('total_collected', '0') or '0'
        total_paid = request.POST.get('total_paid', '0') or '0'
        net_amount = request.POST.get('net_amount', '0') or '0'
        status = request.POST.get('status', '').strip()
        obj = TaxReport(hub_id=hub_id)
        obj.name = name
        obj.period_start = period_start
        obj.period_end = period_end
        obj.total_collected = total_collected
        obj.total_paid = total_paid
        obj.net_amount = net_amount
        obj.status = status
        obj.save()
        return _render_tax_reports_list(request, hub_id)
    return django_render(request, 'tax/partials/panel_tax_report_add.html', {})

@login_required
def tax_report_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TaxReport, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.period_start = request.POST.get('period_start') or None
        obj.period_end = request.POST.get('period_end') or None
        obj.total_collected = request.POST.get('total_collected', '0') or '0'
        obj.total_paid = request.POST.get('total_paid', '0') or '0'
        obj.net_amount = request.POST.get('net_amount', '0') or '0'
        obj.status = request.POST.get('status', '').strip()
        obj.save()
        return _render_tax_reports_list(request, hub_id)
    return django_render(request, 'tax/partials/panel_tax_report_edit.html', {'obj': obj})

@login_required
@require_POST
def tax_report_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(TaxReport, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_tax_reports_list(request, hub_id)

@login_required
@require_POST
def tax_reports_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = TaxReport.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_tax_reports_list(request, hub_id)


@login_required
@with_module_nav('tax', 'settings')
@htmx_view('tax/pages/settings.html', 'tax/partials/settings_content.html')
def settings_view(request):
    return {}

