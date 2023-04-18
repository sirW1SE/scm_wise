# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmDistibutionData(models.Model):
    _name = 'scm.distribution.data'
    _description = "SCM Distribution data"

    product_id = fields.Integer(string='Product_id')
    company_id = fields.Integer(string='Company')
    branch = fields.Char(string='Branch')
    barcode = fields.Char(string='Barcode')
    description = fields.Char(string='Description')
    brand = fields.Char(string='Brand')
    three_mons_sale_qty = fields.Integer(string='3mons sale')
    annually_sale_qty = fields.Integer(string='Annually sale')
    inventory_as_qty = fields.Integer(string='Inventory as of')
    so_number = fields.Char(string='SO Number')


    # _sql_constraints = [
    #     ('warehouse_id_uniq', 'unique (warehouse_id)', 'Tag name already exists!'),
    # ]

    def load_data(self):

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


