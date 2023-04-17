# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmReorder(models.Model):
    _name = 'scm.raw'
    _description = "SCM Reorder"

    sale = fields.Char(string='Sale')
    sale_id = fields.Integer(string='Sale_Id')
    # start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    # def company_data(self):
    #     print("LODLODiitttininininiin")

    #     conn = request.env['scm.config'].scm_conn()
    #     cur = conn.cursor()

    #     comp = '''SELECT id, name FROM res_company'''

    #     cur.execute(comp)


    def load_data(self):
        print("LODLODiitttininininiin")

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        cur.execute('SELECT name, id from sale_order_line where name is not null')
        db_version = cur.fetchall()
        for rec in db_version:
            print(rec)
            self.env['scm.raw'].create({'id': self.id,
                                                'sale': rec[0],
                                                 'sale_id': rec[1]})
        cur.close()

    def get_raw_excel_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/scm_abc_raw/get_raw_excel_report/%s' % (self.id),
            'target': 'new',
        }

        # data = {}
        # print("hahahhahahahha")
        # # return self.env.ref['scm_abc.distribution_report_xlsx_action'].report_action(self, data=data)
        # # return self.env['report'].get_action(self, 'scm_abc.distribution_report_xlsx_action', data=data)


