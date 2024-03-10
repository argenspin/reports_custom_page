from odoo import models,fields,api
from markupsafe import Markup
from odoo.addons.base.models.ir_qweb_fields import nl2br
from collections import defaultdict


#Add new field for storing Accreditations image
class Company(models.Model):
    _inherit = "res.company"
    accreditations = fields.Binary(string="Company Accreditations", help="This field holds the image used to display a accreditations for a given company.")
    company_seal = fields.Binary(string="Company Seal", help="This field holds the image used to display document seal for a given company.")
    
    
    # company_details = fields.Html(string='Company Details', help="Header text displayed at the top of all reports.")

# class ResPartner(models.Model):
#     _inherit = "res.partner"
    
#     def _prepare_display_address(self, without_company=False):
#         # get the information that will be injected into the display format
#         # get the address format
#         address_format = self._get_address_format()
#         args = defaultdict(str, {
#             'state_code': self.state_id.code or '',
#             'state_name': self.state_id.name or '',
#             'country_code': self.country_id.code or '',
#             'country_name': self._get_country_name(),
#             'company_name': self.commercial_company_name or '',
#             'vat' : 'VAT: '+self.vat or '',
#         })
#         for field in self._formatting_address_fields():
#             args[field] = getattr(self, field) or ''
#         if without_company:
#             args['company_name'] = ''
#         elif self.commercial_company_name:
#             address_format = '%(company_name)s\n' + address_format
#         return address_format, args

#That accreditations field should be added to the below model to ensure there are no errors in configuring model layout in settings
class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"
    
    # def _clean_address_format(self, address_format, company_data):
    #     missing_company_data = [k for k, v in company_data.items() if not v]
    #     for key in missing_company_data:
    #         if key in address_format:
    #             address_format = address_format.replace(f'%({key})s\n', '')
    #     return address_format

    # @api.model
    # def _default_company_details(self):
    #     company = self.env.company
    #     address_format, company_data = company.partner_id._prepare_display_address()
    #     address_format = self._clean_address_format(address_format, company_data)
    #     # company_name may *still* be missing from prepared address in case commercial_company_name is falsy
    #     if 'company_name' not in address_format:
    #         address_format = '%(company_name)s\n' + address_format
    #         company_data['company_name'] = company_data['company_name'] or company.name
    #     # print(type(company_data))
    #     #company_data['vat'] = company.vat
    #     #address_format = address_format + '\nVAT: ' + company.vat
    #     return Markup(nl2br(address_format)) % company_data
    
    accreditations = fields.Binary(related = "company_id.accreditations")
    company_seal = fields.Binary(related = "company_id.company_seal")
    # company_details = fields.Html(related='company_id.company_details', readonly=False, default=_default_company_details)


    
