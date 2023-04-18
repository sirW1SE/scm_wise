# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmMasterLiskMcData(models.Model):
    _name = 'scm.master.list.mc.data'
    _description = "SCM MasterList Mc"

    product_id = fields.Integer(string='Product_id')
    barcode = fields.Char(string='Barcode')
    description = fields.Char(string='Description')
    remarks = fields.Char(string='Remarks')
    brand = fields.Char(string='Brand')
    cost = fields.Float(string='Cost')

    def load_master_mc(self):
        print("LODLODiitttininininiin Master list MC")

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        conn.execute('''select t.product_id, b.barcode, c.name, c.brand, t.unit_cost, t.create_date 
                        from (
                          select product_id,
                                 create_date,
                                 unit_cost,
                                 row_number() over (partition by product_id order by create_date desc) as rn
                          from stock_valuation_layer
                        ) t
                        inner join product_product b
                        on b.id = t.product_id
                        inner join product_template c
                        on c.id = b.product_tmpl_id
                        where rn = 1
                        and t.unit_cost <> 0
                        and c.tracking = 'serial'
                        order by b.barcode''')
        db_version = cur.fetchall()
        for rec in db_version:
            s_data=self.env['scm.master.list.mc.data'].search([('product_id','=',rec[0])])
            print('s_data daw', s_data)
            if s_data:
                self.env['scm.master.list.mc.data'].write({'id': self.id,
                                                            'product_id': rec[0],
                                                            'barcode': rec[1],
                                                            'description': rec[2],
                                                            'remarks': '',
                                                            'brand': rec[3],
                                                            'cost': rec[4]})
            else:
                self.env['scm.master.list.mc.data'].create({'id': self.id,
                                                           'product_id': rec[0],
                                                           'barcode': rec[1],
                                                           'description': rec[2],
                                                           'remarks': '',
                                                           'brand': rec[3],
                                                           'cost': rec[4]})


        cur.close()
