# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmMasterLiskMc(models.Model):
    _name = 'scm.master.list.mc'
    _description = "SCM MasterList Mc"

    def get_master_list_mc_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/scm_abc/get_master_list_mc_report/%s' % (self.id),
            'target': 'new',
        }


