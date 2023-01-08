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
            "views/layouts.xml",
            "views/res_company_views.xml",
            "views/paper_format.xml",
            "report/report_layout.xml",
            ],
    "depends": ["base","web","sale"],
}
