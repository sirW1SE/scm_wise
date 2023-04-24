# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from datetime import datetime, timedelta, date
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmDistibution(models.Model):
    _name = 'scm.distribution'
    _description = "SCM Distribution"

    sale = fields.Char(string='Sale')
    sale_id = fields.Integer(string='Sale_Id')
    # start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    def get_dis_excel_report(self):
        self.env['scm.area.code'].load_area()
        return {
            'type': 'ir.actions.act_url',
            'url': '/scm_abc/get_dis_excel_report/%s' % (self.id),
            'target': 'new',
        }

