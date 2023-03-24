# -*- coding: utf-8 -*-
import base64
import io
from odoo import models, fields, api


class distributionXls(models.AbstractModel):
    _name = 'report.scm_abc.distribution_report_to_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx(self, workbook, data, patients):
        print("to xlsx")
