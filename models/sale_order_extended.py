from odoo import fields, models, api
from odoo.fields import Command
from odoo.exceptions import AccessError, UserError, ValidationError
from itertools import groupby


class SaleOrderInherit(models.Model):
    _inherit="sale.order"
    contact_person_id = fields.Many2one('res.partner',string="Person to Contact")
    show_contact_info_pdf = fields.Boolean(string="Show Contact Info on PDF",default=True)
    project_name = fields.Char(string="Project")
    lpo_no = fields.Char(string="LPO No.")
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        return {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_invoice_id.id,
            'sale_order_id': self.env.context.get('active_id'),
            'partner_shipping_id': self.partner_shipping_id.id,
            'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id._get_fiscal_position(self.partner_invoice_id)).id,
            'invoice_origin': self.name, #Added to link name of the sale order to invoice
            'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_user_id': self.user_id.id,
            'payment_reference': self.reference,
            'transaction_ids': [Command.set(self.transaction_ids.ids)],
            'company_id': self.company_id.id,
            'invoice_line_ids': [],
            'project_name': self.project_name,
            'lpo_no': self.lpo_no,
        }

    