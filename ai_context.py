"""
AI context for the Tax module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Tax

### Models

**TaxRate**
- `name` (CharField, max 100): e.g. "IVA 21%", "IVA Reducido 10%", "IVA Superreducido 4%"
- `rate` (Decimal 5,2): percentage value, e.g. `21.00`, `10.00`, `4.00`
- `tax_type` (CharField, default `vat`): type of tax; common values: `vat`, `irpf`, `re`
- `is_default` (bool, default False): only one should be default per hub
- `is_active` (bool, default True)

**TaxReport**
- `name` (CharField): report name/title
- `period_start` / `period_end` (DateField): reporting period
- `total_collected` (Decimal 14,2): tax collected from customers (output VAT)
- `total_paid` (Decimal 14,2): tax paid to suppliers (input VAT)
- `net_amount` (Decimal 14,2): total_collected - total_paid (amount owed to AEAT)
- `status` (CharField, default `draft`): `draft`, `submitted`, `accepted`

### Key flows

**Set up tax rates (Spain):**
- Standard VAT: name="IVA General", rate=21.00, tax_type="vat", is_default=True
- Reduced VAT: name="IVA Reducido", rate=10.00, tax_type="vat"
- Super-reduced VAT: name="IVA Superreducido", rate=4.00, tax_type="vat"

**Generate a tax report:**
1. Create `TaxReport` with period dates and name
2. Calculate `total_collected` from sales/invoices in the period
3. Calculate `total_paid` from expenses in the period
4. Set `net_amount = total_collected - total_paid`
5. Update `status` to `submitted` when filed with AEAT

### Relationships
- TaxRate is referenced by other modules (invoicing, expenses) by rate value, not by FK
- TaxReport is standalone — no FKs to other models
"""
