# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    sourcing_address_id = fields.Many2one(
        'res.partner', string='Sourcing Address',
        related='sale_line_ids.sourcing_address_id')
