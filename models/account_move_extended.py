from odoo import models,fields,api

class AccountMoveExtended(models.Model):
    _inherit="account.move"
    def _get_sale_order_id(self):
        for invoice in self:
            try:
                invoice.sale_order_id = self.env['sale.order'].search([('name','=',invoice.invoice_origin)])[0].id
            except:
                invoice.sale_order_id = 0
            #return sale_order.id or 0
    
    def _get_invoice_type(self):
        for invoice in self:
            invoice.invoice_type = "Down payment"
            for line in invoice.invoice_line_ids:
                if line.product_id.name != "FINAL Payment":
                    invoice.invoice_type = "Regular"
                    break

    sale_order_id=fields.Many2one("sale.order",string="Quotation / Sale Order",compute="_get_sale_order_id")
    invoice_type = fields.Char(string="Invoice Type", compute="_get_invoice_type")

    project_name = fields.Char(string="Project")
    lpo_no = fields.Char(string="LPO No.")
    # field to turn on/off seal on pdf reports
    pdf_seal = fields.Boolean(string="Seal on PDF",default=True)

    def set_lpo_project_name(self):
        invoices = self.env['account.move'].search([])
        for invoice in invoices:
            try:
                sale_order = self.env['sale.order'].search([('name','=',invoice.invoice_origin)])[0]     
                if not invoice.project_name:
                    invoice.project_name = sale_order.project_name
                if not invoice.lpo_no:
                    invoice.lpo_no = sale_order.lpo_no
            except:
                pass

