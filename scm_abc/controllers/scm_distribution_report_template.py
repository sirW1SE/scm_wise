<<<<<<< HEAD
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
=======
# -*- coding: utf-8 -*-
import psycopg2
from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter
from datetime import datetime, timedelta, date


class ScmABCExcelReportController(http.Controller):
    @http.route([
        '/scm_abc/get_dis_excel_report/<model("scm.distribution"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_dis_excel_report(self, wizard=None, **args):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('SCM Report' + '.xlsx'))
            ]
        )

        # print('coooommmppanny:', wizard.company_id)
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

        # sheet 1
        sheet = workbook.add_worksheet('Sheet1')
        # set the orientation to landscape
        sheet.set_landscape()
        # set up the paper size, 9 means A4
        sheet.set_paper(9)
        # set up the margin in inch
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)

        # set up the column width
        sheet.set_column('A:I', 20)
        sheet.set_column('B:B', 60)

        # the report title
        # merge the A1 to E1 cell and apply the style font size : 14, font weight : bold
        sheet.merge_range('A1:D1', 'MC Cost Report as of ' + str(wizard.end_date), title_style)
        # end of sheet1

        # create worksheet/tab per salesperson
        sheet2 = workbook.add_worksheet('Sheet2')
        # set the orientation to landscape
        sheet2.set_landscape()
        # set up the paper size, 9 means A4
        sheet2.set_paper(9)
        # set up the margin in inch
        sheet2.set_margins(0.5, 0.5, 0.5, 0.5)

        # set up the column width
        sheet2.set_column('A:I', 30)

        # the report title
        # merge the A1 to E1 cell and apply the style font size : 14, font weight : bold
        sheet2.merge_range('A1:I1', 'Sales as of ' + str(wizard.end_date), title_style)

        # End of sheet 2

        # start of sheet 3
        sheet3 = workbook.add_worksheet('Sheet3')
        # set the orientation to landscape
        sheet3.set_landscape()
        # set up the paper size, 9 means A4
        sheet3.set_paper(9)
        # set up the margin in inch
        sheet3.set_margins(0.5, 0.5, 0.5, 0.5)

        # set up the column width
        sheet3.set_column('A:E', 20)
        sheet3.set_column('B:B', 60)

        # the report title
        # merge the A1 to E1 cell and apply the style font size : 14, font weight : bold
        sheet3.merge_range('A1:D1', 'Inventory as of ' + str(wizard.end_date), title_style)
        # end of sheet 3

        # sheet 1 column  # table title sheet
        sheet.write(1, 0, 'Barcode', header_style)
        sheet.write(1, 1, 'Description', header_style)
        sheet.write(1, 2, 'Brand', header_style)
        sheet.write(1, 3, 'Cost', header_style)

        row = 2
        number = 1

        # table title sheet 2
        sheet2.write(1, 0, 'Barcode', header_style)
        sheet2.write(1, 1, 'Raw Description', header_style)
        sheet2.write(1, 2, 'Brand', header_style)
        sheet2.write(1, 3, 'Cost', header_style)
        sheet2.write(1, 4, 'Model', header_style)
        sheet2.write(1, 5, 'Branch', header_style)
        sheet2.write(1, 6, 'Last 30D Sale per branch', header_style)
        sheet2.write(1, 7, 'Last 60D Sale per branch', header_style)
        sheet2.write(1, 8, 'Last 90D Sale per branch ', header_style)

        row2 = 2
        number2 = 1

        # sheet3 column # table title sheet 3
        sheet3.write(1, 0, 'Barcode', header_style)
        sheet3.write(1, 1, 'Description', header_style)
        sheet3.write(1, 2, 'Branch', header_style)
        sheet3.write(1, 3, 'Quantity', header_style)

        row3 = 2
        number3 = 1

        conn = request.env['scm.config'].scm_conn()
        cur = conn.cursor()
        cur.execute('''select c.default_code, c.name, c.brand, t.product_id, t.create_date, t.unit_cost
                        from (
                          select product_id,
                                 create_date,
                                 unit_cost,
                                 row_number() over (partition by product_id order by create_date desc) as rn
                          from stock_valuation_layer
                          where unit_cost <> 0
                        ) t
                        left outer join product_product b
                        on b.id = t.product_id
                        inner join product_template c
                        on c.id = b.product_tmpl_id
                        where rn = 1
                        and c.active = true
                        and c.tracking = 'serial'
                        order by c.default_code asc''')

        # display the PostgreSQL database server version
        distribution = cur.fetchall()
        for d_dis in distribution:
            sheet.write(row, 0, d_dis[0], text_style)
            sheet.write(row, 1, d_dis[1], text_style)
            sheet.write(row, 2, d_dis[2], text_style)
            sheet.write(row, 3, d_dis[5], text_style)
            row += 1
            number += 1
        # End of Sheet 1

        cur2 = conn.cursor()
        companies = '(1,2)'
        date_to = wizard.end_date
        cur2.execute('''SELECT c.default_code, c.name as raw_desc, c.brand, c.model, e.name as branch,
                                    COUNT(CASE WHEN (date(b.date_order) >= (date('%s') - interval '30 days') 
                                    AND date(b.date_order) <= '%s') THEN a.product_id end) as ms_a,
                                    COUNT(CASE WHEN (date(b.date_order) >= (date('%s') - interval '60 days') 
                                    AND date(b.date_order) <= '%s') THEN a.product_id end) as ms_b,
                                    COUNT(CASE WHEN (date(b.date_order) >= (date('%s') - interval '90 days') 
                                    AND date(b.date_order) <= '%s') THEN a.product_id end) as ms_c
                                    FROM ((sale_order_line a FULL JOIN sale_order b ON a.order_id = b.id) 
                                    FULL JOIN (product_template c FULL JOIN product_product d 
                                    ON c.id = d.product_tmpl_id) ON a.product_id = d.id), stock_warehouse e 
                                    WHERE a.company_id IN (1,2) AND b.state IN ('sale','done')
                                    AND b.warehouse_id = e.id AND c.type = 'product' AND c.tracking = 'serial'
                                    AND b.date_order BETWEEN (date('%s') - interval '90 days') 
                                    AND ('%s') AND b.partner_id NOT IN (1,8,9)  
                                    GROUP BY c.name, c.brand, c.model, e.name, c.default_code
                                    ORDER by c.name
                        ''' % (date_to, date_to, date_to, date_to, date_to, date_to, date_to, date_to))

        # display the PostgreSQL database server version
        raw = cur2.fetchall()
        for data in raw:
            # the report content
            sheet2.write(row2, 0, data[0], text_style)
            sheet2.write(row2, 1, data[1], text_style)
            sheet2.write(row2, 2, data[2], text_style)
            sheet2.write(row2, 3, '=VLOOKUP(A%s,sheet1!A3:D262, 4, 0)' % (row2 + 1), text_style)
            sheet2.write(row2, 4, data[3], text_style)
            sheet2.write(row2, 5, data[4], text_style)
            sheet2.write(row2, 6, data[5], number_style)
            sheet2.write(row2, 7, data[6], number_style)
            sheet2.write(row2, 8, data[7], number_style)

            row2 += 1
            number2 += 1
        # end of sheet 2
        cur3 = conn.cursor()
        cur3.execute('''WITH sq as (select sq.company_id ppcompany, pt.name, sw.name, pt.brand, pt.default_code as barcode,  
                               sum(sq.quantity) qtybal, sq.product_id as ppproduct, sq.location_id, sl.name, sw.id as swid,
                               pt.id as pptmplid
                               from stock_quant sq
                               inner join product_template pt on sq.product_id = pt.id
                               inner join stock_location sl on sl.id=sq.location_id
                               inner join stock_warehouse sw on sw.lot_stock_id = sl.id
                               inner join res_company rc on rc.id=sq.company_id
                               where pt.tracking = 'serial'
                               and sq.quantity > 0
                               and rc.id IN(1,2)
                               group by pt.name, sq.location_id, pt.default_code, sl.name, sw.name, pt.id, sq.product_id, pt.brand, 
                               sq.location_id, sq.company_id, sw.id
                               order by pt.default_code asc),
                               sw AS (select sw.id as swid, sw.name as wname from  stock_warehouse sw
                                      inner join stock_location sl on sw.lot_stock_id = sl.id
                                      where sw.company_id IN(1,2) 
                                      and sw.active = true),
                               pt AS (select a.id as product_id, b.name as product_name, b.default_code as barcode from product_product a
                                      inner join product_template b on a.product_tmpl_id = b.id
                                      where a.active = true
                                      and b.tracking = 'serial'),
                               dsq AS (select tsq.pptmplid as product_id, tsq.qtybal as qtybal, tsw.wname as wname from sw tsw
                                      left outer join sq tsq on tsq.swid = tsw.swid)
                           select tpt.barcode, tpt.product_name, tdsq.wname, tdsq.qtybal from pt tpt
                           left outer join dsq tdsq on tpt.product_id = tdsq.product_id
                           where tdsq.qtybal > 0
                           order by tpt.barcode''')
        distribution3 = cur3.fetchall()
        for d_dis3 in distribution3:
            # the report content
            sheet3.write(row3, 0, d_dis3[0], text_style)
            sheet3.write(row3, 1, d_dis3[1], text_style)
            sheet3.write(row3, 2, d_dis3[2], text_style)
            sheet3.write(row3, 3, d_dis3[3], text_style)
            row3 += 1
            number3 += 1
        # end of sheet3

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
        cur.close()
        cur2.close()
        cur3.close()
        return response
>>>>>>> 291cf88f137f7da43aafb1270b86f6565dba0dbc
