# from odoo import fields,models,api,_
# from odoo.fields import Command
# from odoo.tools import float_is_zero
# import time



# class SaleAdvancePaymentInvExtended(models.TransientModel):
#     _inherit = 'sale.advance.payment.inv'
#     advance_payment_method = fields.Selection(
#         selection=[
#             ('delivered', "Regular invoice"),
#             ('percentage', "Down payment (percentage)"),
#             ('fixed', "Down payment (fixed amount)"),
#             ('progress', "Progressive payment (percentage)"),
#         ],
#         string="Create Invoice",
#         default='delivered',
#         required=True,
#         help="A standard invoice is issued with all the order lines ready for invoicing,"
#             "according to their invoicing policy (based on ordered or delivered quantity).")

#     progress_amount = fields.Float(
#         string="Progress Payment Amount",
#         help="The percentage of amount to be invoiced as progress , taxes excluded.",default=10.0)

#     def _create_invoices(self, sale_orders):
#         self.ensure_one()
#         if self.advance_payment_method == 'delivered':
#             return sale_orders._create_invoices(final=self.deduct_down_payments)

#         elif self.advance_payment_method == 'progress':
#             self.sale_order_ids.ensure_one()
#             self = self.with_company(self.company_id)
#             order = self.sale_order_ids

#            # Create deposit product if necessary
#             if not self.product_id:
#                 self.product_id = self.env['product.product'].create(
#                     self._prepare_progressive_payment_product_values()
#                 )
#                 self.env['ir.config_parameter'].sudo().set_param(
#                     'sale.default_deposit_product_id', self.product_id.id)

#             # Create down payment section if necessary
#             if not any(line.display_type for line in order.order_line):
#                 self.env['sale.order.line'].create(
#                     self._prepare_progressive_payment_section_values(order)
#                 )

#             progress_payment_so_line = self.env['sale.order.line'].create(
#                 self._prepare_progressive_so_line_values(order)
#             )

#             invoice = self.env['account.move'].sudo().create(
#                 self._prepare_progressive_invoice_values(order, progress_payment_so_line)
#             ).with_user(self.env.uid)  # Unsudo the invoice after creation

#             invoice.message_post_with_view(
#                 'mail.message_origin_link',
#                 values={'self': invoice, 'origin': order},
#                 subtype_id=self.env.ref('mail.mt_note').id)

#             return invoice 




#         else:
#             self.sale_order_ids.ensure_one()
#             self = self.with_company(self.company_id)
#             order = self.sale_order_ids

#             # Create deposit product if necessary
#             if not self.product_id:
#                 self.product_id = self.env['product.product'].create(
#                     self._prepare_down_payment_product_values()
#                 )
#                 self.env['ir.config_parameter'].sudo().set_param(
#                     'sale.default_deposit_product_id', self.product_id.id)

#             # Create down payment section if necessary
#             if not any(line.display_type and line.is_downpayment for line in order.order_line):
#                 self.env['sale.order.line'].create(
#                     self._prepare_down_payment_section_values(order)
#                 )

#             down_payment_so_line = self.env['sale.order.line'].create(
#                 self._prepare_so_line_values(order)
#             )

#             invoice = self.env['account.move'].sudo().create(
#                 self._prepare_invoice_values(order, down_payment_so_line)
#             ).with_user(self.env.uid)  # Unsudo the invoice after creation

#             invoice.message_post_with_view(
#                 'mail.message_origin_link',
#                 values={'self': invoice, 'origin': order},
#                 subtype_id=self.env.ref('mail.mt_note').id)

#             return invoice


#     def _prepare_progressive_payment_product_values(self):
#         self.ensure_one()
#         return {
#             'name': _('Progressive payment'),
#             'type': 'service',
#             'invoice_policy': 'order',
#             'company_id': False,
#             'property_account_income_id': self.deposit_account_id.id,
#             'taxes_id': [Command.set(self.deposit_taxes_id.ids)],
#         }

#     def _prepare_progressive_payment_section_values(self, order):
#         context = {'lang': order.partner_id.lang}

#         so_values = {
#             'name': _('Progressive Payments'),
#             'product_uom_qty': 0.0,
#             'order_id': order.id,
#             'display_type': 'line_section',
#             'is_downpayment': False,
#             'sequence': order.order_line and order.order_line[-1].sequence + 1 or 10,
#         }

#         del context
#         return so_values

#     def _prepare_progressive_so_line_values(self, order):
#         self.ensure_one()
#         analytic_distribution = {}
#         amount_total = sum(order.order_line.mapped("price_total"))
#         if not float_is_zero(amount_total, precision_rounding=self.currency_id.rounding):
#             for line in order.order_line:
#                 distrib_dict = line.analytic_distribution or {}
#                 for account, distribution in distrib_dict.items():
#                     analytic_distribution[account] = distribution * line.price_total + analytic_distribution.get(account, 0)
#             for account, distribution_amount in analytic_distribution.items():
#                 analytic_distribution[account] = distribution_amount/amount_total
#         context = {'lang': order.partner_id.lang}
#         so_values = {
#             'name': _('Progressive Payment: %s (Draft)', time.strftime('%m %Y')),
#             'price_unit': self._get_down_progressive_amount(order),
#             'product_uom_qty': 0.0,
#             'order_id': order.id,
#             'discount': 0.0,
#             'product_id': self.product_id.id,
#             'analytic_distribution': analytic_distribution,
#             'is_downpayment': False,
#             'sequence': order.order_line and order.order_line[-1].sequence + 1 or 10,
#         }
#         del context
#         return so_values

#     def _get_down_progressive_amount(self, order):
#         self.ensure_one()
#         if self.advance_payment_method == 'progress':
#             if all(self.product_id.taxes_id.mapped('price_include')):
#                 progress_amount = order.amount_total * self.progress_amount / 100
#             else:
#                 progress_amount = order.amount_untaxed * self.progress_amount / 100
#         else:  # Fixed amount
#             amount = self.fixed_amount
#         return progress_amount

#     def _prepare_progressive_invoice_values(self, order, so_line):
#         self.ensure_one()
#         return {
#             **order._prepare_invoice(),
#             'invoice_line_ids': [
#                 Command.create(
#                     so_line._prepare_invoice_line(
#                         name=self._get_progressive_payment_description(order),
#                         quantity=1.0,
#                     )
#                 )
#             ],
#         }

#     def _get_progressive_payment_description(self, order):
#         self.ensure_one()
#         context = {'lang': order.partner_id.lang}
#         if self.advance_payment_method == 'progress':
#             name = _("Progressive payment of %s%%", self.progress_amount)
#         else:
#             name = _('Progressive Payment')
#         del context

#         return name