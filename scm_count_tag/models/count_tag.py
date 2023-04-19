# -*- utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.http import request
import odoorpc
import math

LIMIT = 200


class StockCountTag(models.Model):

    _name = 'stock.count.tag'
    _description = 'Count Tag Header Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    location = fields.Selection(
        selection=lambda self: self.get_stock_locations())
    count = fields.Integer(default=0)
    line_ids = fields.One2many(
        comodel_name='stock.count.tag.line', inverse_name='stock_count_tag_id')

    """
        1. add `def init` to setup db details
    """

    # def init(self):
    #     config = self.env['ir.config_parameter']
    #     host = config.get_param('r_host')
    #     port = config.get_param('r_port')
    #     dbname = config.get_param('r_dbname')
    #     user = config.get_param('r_user')
    #     passwd = config.get_param('r_passwd')
    #     if not all(host, port, dbname, user, passwd):
    #         raise UserError(
    #             _('Please contact Administrator for remote configuration.'))

    def connect_remote_psycopg2(self):
        # config = self.env['ir.config_parameter']
        # host = config.get_param('r_host')
        # port = config.get_param('r_port')
        # dbname = config.get_param('r_dbname')
        # user = config.get_param('r_user')
        # passwd = config.get_param('r_passwd')

        # odoo = odoorpc.ODOO(host, port=port)
        # odoo.login(dbname, user, passwd)

        odoo = odoorpc.ODOO('172.104.49.92', port=8079)
        odoo.login('muti_live_copy', 'admin', 'Fy4XoyJMFiqukSzH')

        return odoo

    def get_stock_locations(self):
        odoo = self.connect_remote_psycopg2()
        company_ids = odoo.env['res.company'].search([('name', '!=', 'EPFC')])
        locations = []
        locs = odoo.env['stock.location'].search_read(
            [('usage', '=', 'internal'), ('company_id', 'in', (company_ids)), ('active', '=', True)])
        for loc in locs:
            loc_name = f"{loc.get('id')}"
            locations.append((loc_name, loc.get('complete_name')))
        return locations

    def get_location_name(self):

        ctx = self._context

        print('xctx:', ctx)

        # test = dict(self._fields['location'].selection).get(self.location)
        # print("xtest:", test)

        model = ctx.get('model')
        field = ctx.get('field')
        value = ctx.get('value')

        print("xmodel:", model)
        print("xfield:", field)
        print("xvalue:", value)

        return _(dict(self.env[model].fields_get(allfields=[field])[field]['selection'])[value])

    @api.onchange('location')
    def onchange_location(self):
        first_index = 0
        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        cur.execute("""
        SELECT 
            COUNT(tmpl.id)
        FROM product_template tmpl
        INNER JOIN product_product as prod ON prod.product_tmpl_id = tmpl.id
        INNER JOIN stock_quant as quant ON quant.product_id = prod.id
        INNER JOIN stock_location as loc ON loc.id = quant.location_id
        inner join stock_warehouse sw on sw.lot_stock_id = loc.id
        WHERE tmpl.tracking = 'none' 
        AND tmpl.active = true
        AND quant.location_id = %s
        AND quant.quantity > 0
        AND loc.active = true
        AND loc.usage = 'internal'
        """ % int(self.location))
        products = cur.fetchall()
        print("xxproducts:", products)
        self.update({
            'count': products[first_index][first_index]
        })

    def get_ranges(self):
        ranges = []
        records = self.count
        range_count = math.ceil(records / LIMIT)
        record_count = 0

        for batch in range(0, range_count):
            if batch == 0:
                record_count = batch + LIMIT
                print("rec 1: ", batch, "~", record_count)
                ranges.append((batch, "%s ~ %s" % (batch + 1, record_count)))
            else:
                res = (
                    record_count + LIMIT) > records and records or record_count + LIMIT
                print("rec: ", batch, "~", res)
                ranges.append((record_count, "%s ~ %s" %
                               (record_count + 1, res)))
                record_count = record_count + LIMIT

        return ranges

    @api.onchange('count')
    def create_lines(self):
        index, description = 0, 1
        range_ids = [(5, 0, 0)]
        for rec in self.get_ranges():
            range_ids.append((0, 0, {
                'stock_count_tag_id': self.id,
                'ranges': rec[description],
                'range_value': rec[index],
            }))
        self.line_ids = range_ids


class StockCountTagLine(models.Model):

    _name = 'stock.count.tag.line'
    _description = 'Count Tag Line Model'
    _rec_name = 'ranges'

    stock_count_tag_id = fields.Many2one(
        comodel_name='stock.count.tag', string='Count Tag')
    ranges = fields.Char(string='Ranges')
    range_value = fields.Integer(default=0)
    state = fields.Selection(selection=[(
        'unused', 'Unused'), ('used', 'Used')], default='unused', string='Status')


class CountTagTransient(models.TransientModel):

    _name = 'count.tag.transient'

    stock_count_tag_id = fields.Many2one(
        comodel_name='stock.count.tag', string='Count Tag')
    location = fields.Integer(string="Location")
    series = fields.Integer(string="Series")
    ranges = fields.Many2one(
        comodel_name='stock.count.tag.line', string='Ranges')

    def generate_report(self):
        location_id = self.stock_count_tag_id.location
        print("xlocation_id:", type(location_id))
        print("xlocation_id:", location_id)
        offset = self.ranges.range_value
        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        cur.execute("""
        select 
             prod.barcode, tmpl.brand, tmpl.name, tmpl.part_number, 'PC' as unit, sw.name as branch_name
        FROM product_template tmpl
        INNER JOIN product_product as prod ON prod.product_tmpl_id = tmpl.id
        INNER JOIN stock_quant as quant ON quant.product_id = prod.id
        INNER JOIN stock_location as loc ON loc.id = quant.location_id
        inner join stock_warehouse sw on sw.lot_stock_id = loc.id
        WHERE tmpl.tracking = 'none' 
        AND tmpl.active = true
        AND quant.location_id = %s
        AND quant.quantity > 0
        AND loc.active = true
        AND loc.usage = 'internal'
        ORDER BY prod.barcode ASC LIMIT %s OFFSET %s """ % (location_id, LIMIT, offset))
        stocks = cur.fetchall()

        records = []
        for stock in stocks:
            records.append({
                'barcode': stock[0],
                'brand': stock[1],
                'name': stock[2],
                'part_number': stock[3],
                'unit': stock[4],
                'branch_name': stock[5],
            })

        series = self.series
        location_name = self.stock_count_tag_id.with_context(
            model='stock.count.tag', field='location', value=str(location_id)).get_location_name()
        for rec in records:
            seq_name = "%s-%s" % (location_name.split("/")
                                  [0], str(series).zfill(8))
            rec.update({'tag_no': seq_name})
            series += 1

        data = {
            'records': records
        }
        report_action = self.env.ref(
            'scm_count_tag.report_count_tag').report_action(self, data=data)
        if report_action:
            self.ranges.write({'state': 'used'})

        report_action['close_on_report_download'] = True
        return report_action
