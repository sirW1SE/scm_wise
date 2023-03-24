# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmMasterLiskMc(models.TransientModel):
    _name = 'scm.master.list.mc'
    _description = "SCM MasterList Mc"

    barcode = fields.Char(string='Branch')
    description = fields.Char(string='Branch')
    remarks = fields.Char(string='Branch')
    branch = fields.Char(string='Branch')
    brand = fields.Char(string='Branch')
    old_model_nmae = fields.Char(string='Branch')
    cost = fields.Float(string='Branch')

    def load_data_materlist_mc(self):
        print("LODLODiitttininininiin Master list MC")

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

    def get_master_list_mc_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/scm_abc/get_master_list_mc_report/%s' % (self.id),
            'target': 'new',
        }


