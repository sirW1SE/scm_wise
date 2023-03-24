# -*- coding: utf-8 -*-
import psycopg2
from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter
from odoo import models, fields, api


class ScmABCExcelReportController(http.Controller):
    @http.route([
        '/scm_abc/get_dis_excel_report/<model("scm.distribution"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_sale_excel_report(self, wizard=None, **args):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('ABC Custom Report' + '.xlsx'))
            ]
        )

        # create workbook object from xlsxwriter library
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # create some style to set up the font type, the font size, the border, and the aligment
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'align': 'center'})
        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'left'})
        number_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right'})

        # loop all selected user/salesperson


        # create worksheet/tab per salesperson
        sheet = workbook.add_worksheet('Distribution')
        # set the orientation to landscape
        sheet.set_landscape()
        # set up the paper size, 9 means A4
        sheet.set_paper(9)
        # set up the margin in inch
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)

        # set up the column width
        sheet.set_column('A:A', 8)
        sheet.set_column('B:P', 15)

        # the report title
        # merge the A1 to E1 cell and apply the style font size : 14, font weight : bold
        sheet.merge_range('A1:O1', 'Distribution', title_style)

        # table title
        sheet.write(1, 0, 'Code', header_style)
        sheet.write(1, 1, 'Priority', header_style)
        sheet.write(1, 2, 'Class', header_style)
        sheet.write(1, 3, 'Description', header_style)
        sheet.write(1, 4, 'Branch', header_style)
        sheet.write(1, 5, 'Area', header_style)
        sheet.write(1, 6, 'Brand', header_style)
        sheet.write(1, 7, '3Mo sale', header_style)
        sheet.write(1, 8, 'Annually Sale', header_style)
        sheet.write(1, 9, 'Inventory As of', header_style)
        sheet.write(1, 10, 'BR DoI', header_style)
        sheet.write(1, 11, 'Over all DoI', header_style)
        sheet.write(1, 12, 'Branch Stock Status', header_style)
        sheet.write(1, 13, 'Max Stock (qty)', header_style)
        sheet.write(1, 14, 'Suggest Transfer', header_style)


        row = 2
        number = 1

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()

        cur.execute('''select a.id, d.name as company, b.name as product, g.name as branch, b.brand as brand, f.complete_name as stocklocation, a.barcode, a.default_code, sum(e.quantity), 
                            e.location_id, f.name
                            from product_product a, product_template b, stock_production_lot c, res_company d, stock_quant e,
                            stock_location f, stock_warehouse g
                            where b.id = a.product_tmpl_id
                            and b.id = c.product_id
                            and d.id = c.company_id
                            and c.id = e.lot_id
                            and f.id = e.location_id
                            and g.lot_stock_id = f.id
                            and c.company_id = 2
                            group by d.name,product,branch,f.complete_name,a.barcode, brand,
							a.default_code,e.location_id,f.name,a.id, e.quantity order by a.id asc''')


        # display the PostgreSQL database server version
        distribution = cur.fetchall()
        for d_dis in distribution:
            print(d_dis)
            # the report content
            sheet.write(row, 0, '', text_style)
            sheet.write(row, 1, '', text_style)
            sheet.write(row, 2, '', text_style)
            sheet.write(row, 3, d_dis[2], text_style)
            sheet.write(row, 4, d_dis[3], text_style)
            sheet.write(row, 5, '', text_style)
            sheet.write(row, 6, d_dis[4], text_style)
            sheet.write(row, 7, '', text_style)
            sheet.write(row, 8, '', text_style)
            sheet.write(row, 9, d_dis[8], text_style)
            sheet.write(row, 10, '', text_style)
            sheet.write(row, 11, '', text_style)
            sheet.write(row, 12, '', text_style)
            sheet.write(row, 13, '', text_style)
            sheet.write(row, 14, '', text_style)

            row += 1
            number += 1

        # return the excel file as a response, so the browser can download it
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        cur.close()
        return response

        # conn = None
        # p_data = []
        # try:
        #     conf = request.env['scm.config'].search([('active', '=', True)], limit=1)
        #     print("connection dndbdbddbdbdb: ", conf.port)
        #
        #     params = {
        #         'host': conf.host,
        #         'dbname': conf.database,
        #         'port': conf.port,
        #         'user': conf.user,
        #         'password': conf.password
        #     }
        #
        #     # read connection parameters
        #     # conn =
        #     # params = conn
        #     # print('From Config Connecting to the PostgreSQL database...', params)
        #
        #     # connect to the PostgreSQL server
        #     print('Connecting to the PostgreSQL database...')
        #     conn = psycopg2.connect(**params)
        #
        #     # create a cursor
        #     cur = conn.cursor()
        #
        #     # execute a statement
        #     print('PostgreSQL database version:')
        #     cur.execute("""select c.company_id, d.name, a.id, a.barcode, a.default_code, b.name, c.name, e.quantity,
        #                                      e.location_id, f.name, f.complete_name, g.name
        #                                      from product_product a, product_template b, stock_production_lot c, res_company d, stock_quant e,
        #                                      stock_location f, stock_warehouse g
        #                                      where b.id = a.product_tmpl_id
        #                                      and b.id = c.product_id
        #                                      and d.id = c.company_id
        #                                      and c.id = e.lot_id
        #                                      and f.id = e.location_id
        #                                      and g.lot_stock_id = f.id
        #                                      and c.company_id = 2
        #                                      and f.name = 'Stock'
        #                                      order by a.id asc""")
        #
        #     # display the PostgreSQL database server version
        #     purchase = cur.fetchall()
        #     for com in purchase:
        #         # pp = p_data.append(com)
        #         # print(com)
        #         print(com[2], com[10], com[9], com[6], com[7], com[8])
        #         # print(p_data)
        #     # self.po_number = p_data
        #
        #     # print(db_version)
        #
        #     # search the sales order
        #     # orders = request.env['sale.order'].search(
        #     #     [('company_id', '=', company.id), ('date_order', '>=', wizard.start_date),
        #     #      ('date_order', '<=', wizard.end_date)])
        #     # for order in orders:
        #     #     # the report content
        #     #     sheet.write(row, 0, number, text_style)
        #     #     sheet.write(row, 1, order.name, text_style)
        #     #     sheet.write(row, 2, str(order.date_order), text_style)
        #     #     sheet.write(row, 3, order.partner_id.name, text_style)
        #     #     sheet.write(row, 4, order.amount_total, number_style)
        #     #
        #     #
        #     #     row += 1
        #     #     number += 1
        #
        #     # close the communication with the PostgreSQL
        #     cur.close()
        # except (Exception, psycopg2.DatabaseError) as error:
        #     print(error)
        # finally:
        #     if conn is not None:
        #         conn.close()
        #         print('Database connection closed.')
