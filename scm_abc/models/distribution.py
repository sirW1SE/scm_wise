<<<<<<< HEAD
# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmDistibution(models.TransientModel):
    _name = 'scm.distribution'
    _description = "SCM Distribution"

    branch = fields.Char(string='Branch')
    warehouse_id = fields.Integer(string='Warehou_id')

    _sql_constraints = [
        ('warehouse_id_uniq', 'unique (warehouse_id)', 'Tag name already exists!'),
    ]

    def load_data(self):
        print("LODLODiitttininininiin")

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        cur.execute('SELECT name, partner_id from res_company where name is not null')
        db_version = cur.fetchall()
        for rec in db_version:
            print(rec)
            self.env['scm.distribution'].create({'id': self.id,
                                                 'branch': rec[0],
                                                 'warehouse_id': rec[1]})
        cur.close()

    def get_dis_excel_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/scm_abc/get_dis_excel_report/%s' % (self.id),
            'target': 'new',
        }

        # data = {}
        # print("hahahhahahahha")
        # # return self.env.ref['scm_abc.distribution_report_xlsx_action'].report_action(self, data=data)
        # # return self.env['report'].get_action(self, 'scm_abc.distribution_report_xlsx_action', data=data)


=======
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
        return {
            'type': 'ir.actions.act_url',
            'url': '/scm_abc/get_dis_excel_report/%s' % (self.id),
            'target': 'new',
        }

>>>>>>> 291cf88f137f7da43aafb1270b86f6565dba0dbc
