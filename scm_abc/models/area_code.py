# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmAreaCode(models.Model):
    _name = 'scm.area.code'
    _description = "Area Code"

    branch_id = fields.Integer(string='Branch ID')
    branch_name = fields.Char(string='Barcode')
    area_code = fields.Char(string='Area Code')

    def loadinit(self):

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        cur.execute('''select f.id, g.name as branch, f.complete_name as stocklocation
                            from stock_location f, stock_warehouse g
                            where g.lot_stock_id = f.id
                            group by branch,f.complete_name, f.id order by stocklocation asc''')
        db_version = cur.fetchall()
        for rec in db_version:
            s_data=self.env['scm.area.code'].search([('branch_id','=',rec[0])])
            print('s_data daw', s_data)
            if s_data:
                self.env['scm.area.code'].write({'id': self.id,
                                                            'branch_id': rec[0],
                                                            'branch_name': rec[1]
                                                            })
            else:
                self.env['scm.area.code'].create({'id': self.id,
                                                           'branch_id': rec[0],
                                                           'branch_name': rec[1]
                                                           })


        cur.close()

