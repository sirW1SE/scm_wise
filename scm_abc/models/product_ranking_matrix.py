# -*- coding: utf-8 -*-
import psycopg2
from odoo import models, fields, api, tools
from odoo.http import content_disposition, request
import io
import xlsxwriter
from xlsxwriter import workbook


class ScmProductRankingMatrix(models.Model):
    _name = 'scm.product.ranking.matrix'
    _description = "Product Ranking Matrix"

    code = fields.Char(string='Code')
    priority = fields.Integer(string='Priority')
    lt_supply = fields.Char(string='LT(supply)')
    ss_supply = fields.Char(string='SS')
    max_stock_supply = fields.Char(string='Max Stock')
    lt_branch = fields.Integer(string='LT(branch)')
    ss_branch = fields.Char(string='SS(branch)')
    max_stock_branch = fields.Char(string='Max Stock Branch')
    product_class = fields.Char(string='Class')