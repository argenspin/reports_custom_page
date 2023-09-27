# Copyright 2015 Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Reports Custom Page",
    "version": "1.0",
    "author": "DataSoup",
    "category": "Tools",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "data": [
            "views/invoice_form.xml",
            "views/layouts.xml",
            "views/custom_header_footer.xml",
            "views/res_company_views.xml",
            "views/paper_format.xml",
            "views/invoice_layout.xml",
            "report/purchase_report_layout.xml",
            "report/report_layout.xml",
            "report/stock_delivery_report_layout.xml",
            "report/ir_actions_report.xml",
            ],
    "depends": ["base","web","sale","account"],
}
