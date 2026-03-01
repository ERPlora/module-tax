"""AI tools for the Tax module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListTaxRates(AssistantTool):
    name = "list_tax_rates"
    description = "List tax rates."
    module_id = "tax"
    required_permission = "tax.view_taxrate"
    parameters = {"type": "object", "properties": {"is_active": {"type": "boolean"}, "tax_type": {"type": "string"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from tax.models import TaxRate
        qs = TaxRate.objects.all()
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        if args.get('tax_type'):
            qs = qs.filter(tax_type=args['tax_type'])
        return {"rates": [{"id": str(r.id), "name": r.name, "rate": str(r.rate), "tax_type": r.tax_type, "is_default": r.is_default, "is_active": r.is_active} for r in qs]}


@register_tool
class CreateTaxRate(AssistantTool):
    name = "create_tax_rate"
    description = "Create a tax rate."
    module_id = "tax"
    required_permission = "tax.add_taxrate"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "rate": {"type": "string"}, "tax_type": {"type": "string"}, "is_default": {"type": "boolean"}},
        "required": ["name", "rate"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from tax.models import TaxRate
        r = TaxRate.objects.create(name=args['name'], rate=Decimal(args['rate']), tax_type=args.get('tax_type', 'vat'), is_default=args.get('is_default', False))
        return {"id": str(r.id), "name": r.name, "created": True}


@register_tool
class ListTaxReports(AssistantTool):
    name = "list_tax_reports"
    description = "List tax reports."
    module_id = "tax"
    required_permission = "tax.view_taxreport"
    parameters = {"type": "object", "properties": {"status": {"type": "string"}, "limit": {"type": "integer"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from tax.models import TaxReport
        qs = TaxReport.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {"reports": [{"id": str(r.id), "name": r.name, "period_start": str(r.period_start), "period_end": str(r.period_end), "total_collected": str(r.total_collected), "total_paid": str(r.total_paid), "net_amount": str(r.net_amount), "status": r.status} for r in qs.order_by('-period_start')[:limit]]}
